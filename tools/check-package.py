#!/usr/bin/env python3
"""Compare a built .pkg.tar.zst to the current manifest and source bytes.

Reads the archive without extracting it. Verifies root ownership, file modes,
all symlink texts/targets, required dependencies, and absence of extra payload.
"""
import argparse
from pathlib import Path, PurePosixPath
import posixpath
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parent.parent
NAME = 'plasma6-themes-nobara-fixed'
FORBIDDEN = ('usr/share/aurorae/', 'usr/share/sddm/', 'usr/share/polkit-1/',
             'usr/share/themes/Nobara/gtk-2.0/', 'usr/share/themes/Nobara/assets/',
             'usr/share/plasma/desktoptheme/Nobara/_templates/',
             'usr/share/plasma/look-and-feel/org.nobaraproject.desktop/contents/lockscreen/',
             'usr/share/plasma/plasmoids/com.kde.plasma.nobara.runcommand/')
DOCS = ('README.md', 'CHANGELOG.md', 'AUDIT.md', 'SOURCE.txt',
        'UPSTREAM-NOTICES.md', 'ICONS.md', 'PLASMA-LOGIN.md',
        'PERFORMANCE.md', 'PACKAGING.md')


def expected_files():
    expected = {}
    for raw in (ROOT / 'packaging/install-manifest.txt').read_text().splitlines():
        resource = raw.strip()
        if not resource or resource.startswith('#'):
            continue
        parts = PurePosixPath(resource).parts
        if not resource.startswith('usr/share/') or '..' in parts:
            raise ValueError(f'Unsafe install manifest entry: {resource}')
        path = ROOT / resource
        if not path.exists():
            raise ValueError(f'Missing manifest entry: {resource}')
        for file in [path, *sorted(path.rglob('*'))] if path.is_dir() else [path]:
            if file.is_symlink() or file.is_file():
                key = file.relative_to(ROOT).as_posix()
                if key.startswith(FORBIDDEN) or key.endswith(('nobara-apply-theme.sh', 'nobara-clean-theme.sh')):
                    raise ValueError(f'Excluded component in manifest: {key}')
                if key in expected:
                    raise ValueError(f'Overlapping install manifest: {key}')
                expected[key] = file
    for doc in DOCS:
        expected[f'usr/share/doc/{NAME}/{doc}'] = ROOT / doc
    expected[f'usr/share/doc/{NAME}/install-manifest.txt'] = ROOT / 'packaging/install-manifest.txt'
    expected[f'usr/share/licenses/{NAME}/LICENSE'] = ROOT / 'LICENSE'
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path, nargs='?')
    parser.add_argument('--source', action='store_true', help='check the source install manifest only')
    args = parser.parse_args()
    if args.source == bool(args.package):
        parser.error('provide either --source or a package archive')
    expected = expected_files()
    if args.source:
        print(f'SOURCE MANIFEST PASSED: {len(expected)} files/links; excluded components absent.')
        return
    seen = set()
    links = []
    metadata = {}
    errors = []
    process = subprocess.Popen(['zstd', '-dc', '--', str(args.package)], stdout=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=process.stdout, mode='r|') as tar:
            for item in tar:
                key = item.name.removeprefix('./').rstrip('/')
                if not key:
                    continue
                if key.startswith('/') or '..' in PurePosixPath(key).parts:
                    raise ValueError(f'Unsafe archive path: {key}')
                if item.uid != 0 or item.gid != 0:
                    errors.append(f'Non-root ownership: {key}')
                if item.isdir():
                    if item.mode != 0o755:
                        errors.append(f'Unexpected directory mode: {key}')
                    if not any(p.startswith(key + '/') for p in expected):
                        errors.append(f'Unexpected directory: {key}')
                    continue
                if key in seen:
                    errors.append(f'Duplicate archive entry: {key}')
                seen.add(key)
                if key in ('.PKGINFO', '.BUILDINFO', '.MTREE') and item.isfile():
                    metadata[key] = tar.extractfile(item).read()
                    continue
                source = expected.get(key)
                if source is None:
                    errors.append(f'Unexpected payload: {key}')
                    continue
                if source.is_symlink():
                    if not item.issym() or item.mode != 0o777 or item.linkname != source.readlink().as_posix():
                        errors.append(f'Changed icon link: {key}')
                    else:
                        links.append((key, item.linkname))
                elif not item.isfile() or item.mode != 0o644 or tar.extractfile(item).read() != source.read_bytes():
                    errors.append(f'Changed bytes/type/mode: {key}')
        if process.wait() != 0:
            errors.append('Could not decompress package')
    finally:
        process.stdout.close()
        if process.poll() is None:
            process.terminate()
            process.wait()
    errors.extend(f'Missing payload: {key}' for key in sorted(set(expected) - seen))
    errors.extend(f'Missing package metadata: {key}' for key in ('.PKGINFO', '.BUILDINFO', '.MTREE') if key not in metadata)
    for key, target in links:
        if target.startswith('/'):
            if not target.startswith(('/usr/share/icons/Papirus/', '/usr/share/icons/Papirus-Dark/')) or not Path(target).is_file():
                errors.append(f'Missing/unexpected external icon: {key} -> {target}')
        elif posixpath.normpath(posixpath.join(posixpath.dirname(key), target)) not in expected:
            errors.append(f'Broken internal package link: {key} -> {target}')
    info = metadata.get('.PKGINFO', b'').decode()
    for line in (f'pkgname = {NAME}', 'arch = any',
                 'depend = plasma-workspace>=6.8', 'depend = plasma-desktop>=6.8',
                 'depend = breeze>=6.8', 'depend = breeze-cursors>=6.8',
                 'depend = breeze-gtk>=6.8', 'depend = papirus-icon-theme>=20260801'):
        if line not in info.splitlines():
            errors.append(f'Missing package metadata: {line}')
    if errors:
        raise SystemExit('PACKAGE CHECK FAILED\n' + '\n'.join(errors))
    print(f'PACKAGE CHECK PASSED: {len(expected)} files/links, {len(links)} intact icon links; exact manifest, bytes, modes, ownership and dependencies.')


if __name__ == '__main__':
    main()
