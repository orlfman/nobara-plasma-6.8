#!/usr/bin/env python3
"""Snapshot this working tree, checksum the local source, and refresh .SRCINFO.

Includes uncommitted changes. Does not build/install or access the network.
Symlinks are archived as links, never followed into installed Papirus artwork.
"""
import gzip
import hashlib
import io
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'packaging'
DOCS = ('README.md', 'CHANGELOG.md', 'AUDIT.md', 'SOURCE.txt',
        'UPSTREAM-NOTICES.md', 'ICONS.md', 'PLASMA-LOGIN.md',
        'PERFORMANCE.md', 'PACKAGING.md', 'AGENTS.md', 'CLAUDE.md', 'PLAN.md',
        'CONTRIBUTING.md')


def main():
    recipe = BUILD / 'PKGBUILD'
    text = recipe.read_text()
    name = re.search(r'^pkgname=([a-z0-9.+-]+)$', text, re.M).group(1)
    version = re.search(r'^pkgver=([a-zA-Z0-9.+_]+)$', text, re.M).group(1)
    stem = f'{name}-{version}'
    archive = BUILD / f'{stem}.tar.gz'
    epoch = int(os.environ.get('SOURCE_DATE_EPOCH', '0'))
    paths = [ROOT / item for item in (*DOCS, 'LICENSE', 'usr', 'tools',
                                     'packaging/install-manifest.txt')]
    entries = set()
    for path in paths:
        if not path.exists():
            raise SystemExit(f'Missing source: {path}')
        entries.add(path)
        if path.is_dir():
            entries.update(p for p in path.rglob('*')
                           if '__pycache__' not in p.parts and p.suffix != '.pyc')
    # Reading files and creating tar headers explicitly avoids following symlinks
    # and normalizes metadata, independent of checkout timestamps/ownership.
    with tempfile.NamedTemporaryFile(dir=BUILD, prefix='.source-', delete=False) as tmp:
        temporary = Path(tmp.name)
        try:
            with gzip.GzipFile(fileobj=tmp, mode='wb', filename='', mtime=epoch) as gz:
                with tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as tar:
                    for path in sorted(entries):
                        rel = path.relative_to(ROOT)
                        info = tar.gettarinfo(str(path), f'{stem}/{rel.as_posix()}')
                        info.uid = info.gid = 0
                        info.uname = info.gname = 'root'
                        info.mtime = epoch
                        info.mode = 0o755 if info.isdir() or (not info.issym() and os.access(path, os.X_OK)) else 0o644
                        if info.isfile():
                            tar.addfile(info, io.BytesIO(path.read_bytes()))
                        elif info.isdir() or info.issym():
                            if info.issym():
                                info.mode = 0o777
                            tar.addfile(info)
                        else:
                            raise SystemExit(f'Unsupported source file: {rel}')
            tmp.flush()
            temporary.replace(archive)
            archive.chmod(0o644)
        finally:
            temporary.unlink(missing_ok=True)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    text, count = re.subn(r"^sha256sums=\('[^']*'\)$",
                         f"sha256sums=('{digest}')", text, flags=re.M)
    if count != 1:
        raise SystemExit('Expected exactly one sha256sums entry in PKGBUILD')
    recipe.write_text(text)
    srcinfo = subprocess.check_output(['makepkg', '--printsrcinfo'], cwd=BUILD, text=True)
    (BUILD / '.SRCINFO').write_text(srcinfo)
    print(f'Source: {archive}')
    print(f'SHA256: {digest}')
    print('Updated packaging/PKGBUILD and packaging/.SRCINFO. No installation.')


if __name__ == '__main__':
    main()
