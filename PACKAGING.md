# Local Arch packaging

The local package is `plasma6-themes-nobara-fixed`, version `0.1.0-1`, architecture
`any`. This is the adaptation's own version, not Nobara's upstream version or a
Plasma version. The name is a local working name; no AUR name has been reserved.
No package is installed or uploaded by the preparation/build commands below.

## Installed contents and dependencies

`packaging/install-manifest.txt` explicitly lists runtime files/directories.
It includes Plasma appearance, the optional panel layout/widget, all retained
wallpapers, the Papirus-inheriting icon overlay and three branding icons,
Plasma Login wallpaper, GTK 3/4 and Konsole appearance, plus documentation and
license notices. Links to Papirus remain links; its artwork is not copied.
Aurorae's unrepaired flat layout and desktoptheme `_templates` stay in the
source archive for later work and are excluded from the binary package.
No `/etc`, GTK 2, SDDM, custom polkit/service/helper files or installation scripts
are shipped. Normal distribution icon-cache hooks can run during installation.

Required dependencies are `plasma-workspace>=6.8`, `plasma-desktop>=6.8`,
`breeze>=6.8`, `breeze-cursors>=6.8`, `breeze-gtk>=6.8`, and
`papirus-icon-theme>=20260801`. Plasma Desktop supplies the normal panel applets;
Breeze supplies widgets/decorations, and the separately packaged Breeze cursors
satisfy the global theme's cursor reference. Papirus is mandatory, as requested.
The exact tested versions and remaining live-testing limits are in
[PERFORMANCE.md](PERFORMANCE.md) and [AUDIT.md](AUDIT.md).

Optional consumers are `konsole` and `plasma-login-manager`. Installing this
package does not enable or switch a display manager. Python is only a build
check dependency. Standard Arch `base-devel` tools are needed to build; the
additional developer/runtime checks also need the tools described in AGENTS.md.

## Prepare and build

Run from the repository root (`nobara-plasma-6.8` after cloning):

```sh
python3 -I tools/prepare-package.py
cd packaging
makepkg --cleanbuild --clean
```

The helper snapshots the **current working tree, including uncommitted changes**,
into `packaging/plasma6-themes-nobara-fixed-0.1.0.tar.gz`. It includes retained
source artwork, tools, notices and project notes. It excludes `.git`, build
output and Python caches. It sets normalized ownership/modes/timestamps and gzip
headers, producing the same source checksum for unchanged inputs. Source
mtime defaults to zero; `SOURCE_DATE_EPOCH` can set it explicitly.
The PKGBUILD and generated `.SRCINFO` sit beside the source archive, outside it,
to avoid a circular checksum. The helper writes the real SHA-256 into both.
Rerun preparation after changes; do not use `SKIP` for integrity checks.

`makepkg` verifies that checksum and runs the source manifest, theme and icon checks. It builds
`packaging/plasma6-themes-nobara-fixed-0.1.0-1-any.pkg.tar.zst` with the default
Arch configuration. A custom `PKGDEST` or package extension can change its path.
These commands do not install missing dependencies: install build requirements
separately if needed. No root privileges or network are needed once they exist.

Verify the resulting package against this working tree:

```sh
python3 -I tools/check-package.py packaging/plasma6-themes-nobara-fixed-0.1.0-1-any.pkg.tar.zst
namcap packaging/PKGBUILD packaging/plasma6-themes-nobara-fixed-0.1.0-1-any.pkg.tar.zst
```

The package checker compares the full payload with the explicit manifest and
current source bytes, icon links, permissions, ownership and dependencies. A
later working-tree edit intentionally makes the old package fail that comparison;
prepare and rebuild to refresh it. It never extracts into the live filesystem.

## Validation notes

The local build and exact-content comparison pass, with 1,950 files/links and
all 1,705 icon links preserved. The extracted package also passes KDE package,
wallpaper, Plasma-style and icon-loader probes in temporary isolated settings.
Structural/GTK/QML checks, four icon-builder recovery cases, four controller
behavior cases plus init/cleanup, and the splash idle regression pass.

`namcap` reports no errors. Its ten warnings cover five dependencies already
provided transitively by Plasma/Papirus (`kirigami`, `hicolor-icon-theme`,
`libplasma`, `qt6-declarative`, `ksvg`) and five appearance dependencies it
cannot establish from theme settings, CSS imports, panel layouts or external
icon links (`plasma-desktop`, `breeze`, `breeze-cursors`, `breeze-gtk`,
`papirus-icon-theme`). These references were checked manually; keep those
appearance dependencies. This was built on the existing CachyOS installation,
not in a clean Arch build environment. A live desktop/login test remains pending.

## Install, select and remove

After reviewing the package, install explicitly:

```sh
sudo pacman -U packaging/plasma6-themes-nobara-fixed-0.1.0-1-any.pkg.tar.zst
```

Pacman handles required dependencies through the configured repositories. If a
required dependency is unavailable there, resolve that before installing.
Select Nobara through System Settings as described in [README.md](README.md).
Panel replacement remains an explicit choice. Select GTK appearance and Konsole
colors separately. For Plasma Login, follow [PLASMA-LOGIN.md](PLASMA-LOGIN.md)
after installation; resources must be readable by its separate login account.
Installation does not apply any of these settings automatically.

Before removal, select another global theme, icons, Plasma style, wallpaper,
GTK theme and Konsole color/profile wherever Nobara is selected. If Nobara is
used at login, select another desktop appearance and explicitly synchronize it
through Plasma Login's settings, then choose a replacement login wallpaper.
If using the Nobara panel widget, remove it or replace it with a stock desktop
widget before removal. Then remove the package:

```sh
sudo pacman -R plasma6-themes-nobara-fixed
```

Removal leaves personal settings and required dependencies alone. It cannot
restore prior selections because the package never records or changes them.

## Later publication

This recipe intentionally uses a local checksummed source archive. Before AUR
submission, create an authorized pinned source release in
[the GitHub project](https://github.com/orlfman/nobara-plasma-6.8), review the
package name and version, replace `source` with its downloadable release URL
and real checksum, regenerate `.SRCINFO`, and
validate in a clean Arch build environment. Do not upload this local-only recipe
as though its source were publicly downloadable. The GitHub source repository
is public; no release or AUR publication has been made.

Packaging conventions follow the official
[PKGBUILD manual](https://man.archlinux.org/man/PKGBUILD.5.en) and
[makepkg manual](https://man.archlinux.org/man/makepkg.8.en).
