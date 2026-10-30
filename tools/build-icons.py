#!/usr/bin/env python3
"""Build/check Nobara's Papirus-Dark overlay without modifying Papirus.

The virtual folder replacements match papirus-folders' violet operation.
Following aliases also covers inherited names such as folder-downloads and
inode-directory, which would otherwise resolve to the unchanged blue parent.
"""
import argparse
import configparser
from functools import lru_cache
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BASE = Path('/usr/share/icons/Papirus-Dark')
OUTPUT = ROOT / 'usr/share/icons/Nobara'
BRANDING = {
    'scalable/places/nobara-app-menu-icon.svg': '../../../hicolor/scalable/places/nobara-app-menu-icon.svg',
    'scalable/actions/nobara-desktop-show-symbolic.svg': '../../../hicolor/scalable/actions/nobara-desktop-show-symbolic.svg',
    'scalable/actions/nobara-desktop-hide-symbolic.svg': '../../../hicolor/scalable/actions/nobara-desktop-hide-symbolic.svg',
}


def read_config(path):
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    with path.open() as stream:
        config.read_file(stream)
    return config


def expected():
    config = read_config(BASE / 'index.theme')
    header = config['Icon Theme']
    directories = header['Directories'].split(',') + header.get('ScaledDirectories', '').split(',')
    directories = list(dict.fromkeys(d for d in directories if d))
    replacements = {}
    # Use only real violet files, as the upstream helper does; retain alias chains.
    for size in (22, 24, 32, 48, 64):
        folder = BASE / f'{size}x{size}/places'
        for prefix in ('folder-violet', 'user-violet'):
            for path in folder.glob(prefix + '*.svg'):
                if path.is_symlink() or not path.is_file():
                    continue
                generic = path.name.replace('-violet', '', 1)
                replacements[folder.resolve() / generic] = str(path.resolve())
    if not replacements:
        raise ValueError('papirus-icon-theme is missing its violet folder artwork')

    @lru_cache(maxsize=None)
    def canonical_parent(parent):
        return parent.resolve()

    @lru_cache(maxsize=None)
    def replacement(path, depth=0):
        if depth > 40:
            raise ValueError(f'icon symlink loop: {path}')
        key = canonical_parent(path.parent) / path.name
        if key in replacements:
            return replacements[key]
        if key.is_symlink():
            target = Path(os.path.normpath(key.parent / os.readlink(key)))
            return replacement(target, depth + 1)
        return None

    links = dict(BRANDING)
    selected = {}
    # Reuse directory scans for Papirus's shared/high-DPI directory aliases.
    @lru_cache(maxsize=None)
    def files(folder):
        return tuple(sorted(p.name for p in folder.glob('*.svg')))

    for directory in directories:
        folder = BASE / directory
        for name in files(folder.resolve()):
            target = replacement(folder / name)
            if target is not None:
                links[f'{directory}/{name}'] = target
                selected[directory] = dict(config[directory])

    # A child theme otherwise scales its 22px folder over the parent's native
    # 16px icon. Keep Papirus Dark's small monochrome forms unchanged.
    names = {Path(name).name for name in links if not name.startswith('scalable/')}
    for directory in directories:
        if config.get(directory, 'Size', fallback='') != '16' or config.get(directory, 'Context', fallback='') != 'Places' or 'symbolic' in directory:
            continue
        for name in sorted(names):
            path = BASE / directory / name
            if path.is_file():
                links[f'{directory}/{name}'] = str(path.resolve())
                selected[directory] = dict(config[directory])

    selected['scalable/places'] = {'Context': 'Places', 'Size': '48', 'MinSize': '16', 'MaxSize': '512', 'Type': 'Scalable'}
    selected['scalable/actions'] = {'Context': 'Actions', 'Size': '16', 'MinSize': '16', 'MaxSize': '512', 'Type': 'Scalable'}
    regular = [d for d in selected if config.get(d, 'Scale', fallback='1') == '1']
    scaled = [d for d in selected if config.get(d, 'Scale', fallback='1') != '1']
    lines = ['[Icon Theme]', 'Name=Nobara',
             'Comment=Papirus Dark with violet folders and Nobara branding',
             'Inherits=Papirus-Dark', 'Example=folder', 'FollowsColorScheme=true',
             'Directories=' + ','.join(regular)]
    if scaled:
        lines.append('ScaledDirectories=' + ','.join(scaled))
    for directory, values in selected.items():
        lines.extend(['', f'[{directory}]', *(f'{key}={value}' for key, value in values.items())])
    return '\n'.join(lines) + '\n', links


def verify(index, links):
    failures = []
    if not (OUTPUT / 'index.theme').is_file() or (OUTPUT / 'index.theme').read_text() != index:
        failures.append('index.theme is missing or outdated')
    actual = {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob('*') if p.is_symlink() or p.is_file()}
    if actual != set(links) | {'index.theme'}:
        failures.append('overlay file inventory differs from installed Papirus; rebuild it')
    for name, target in links.items():
        path = OUTPUT / name
        if not path.is_symlink() or os.readlink(path) != target:
            failures.append(f'wrong icon link: {name}')
        elif not path.is_file():
            failures.append(f'missing icon dependency: {name} -> {target}')
    if failures:
        raise ValueError('\n'.join(failures[:12]))


def validate_targets(links):
    """Reject missing dependencies before replacing an existing overlay."""
    for name, target in links.items():
        path = Path(target) if os.path.isabs(target) else OUTPUT.joinpath(name).parent / target
        if not path.is_file():
            raise ValueError(f'missing icon dependency: {name} -> {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--build', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    index, links = expected()
    if args.build:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        validate_targets(links)
        if OUTPUT.is_symlink():
            raise ValueError('refusing to replace a symlinked output directory')
        # Preserve the old output if publishing fails; never touch the base.
        work = Path(tempfile.mkdtemp(prefix='.nobara-icons-', dir=OUTPUT.parent))
        backup = work / 'old'
        published = False
        try:
            stage = work / 'Nobara'
            stage.mkdir()
            (stage / 'index.theme').write_text(index)
            for name, target in links.items():
                path = stage / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(target)
            if OUTPUT.exists():
                OUTPUT.rename(backup)
            try:
                stage.rename(OUTPUT)
            except OSError:
                if backup.exists():
                    backup.rename(OUTPUT)
                raise
            published = True
        finally:
            if published or not backup.exists():
                shutil.rmtree(work)
            else:
                print(f'Previous icon theme preserved for recovery at {backup}', file=sys.stderr)
    verify(index, links)
    print(f'Nobara icon inheritance, aliases and targets: PASS ({len(links)} links)')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, configparser.Error) as exc:
        sys.exit(str(exc))
