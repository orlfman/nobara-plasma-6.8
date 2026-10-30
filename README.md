# Nobara - Plasma 6.8

Nobara's KDE Plasma appearance, adapted and checked against **Plasma 6.8.2**,
with its wallpapers, Papirus-based icons, GTK 3/4 and Konsole themes.

Based on Nobara's `kde-nobara` 6.7.5. This is an unofficial appearance-only
adaptation: it keeps Nobara's artwork and colors without its distribution
configuration, setup scripts, polkit rules or systemd units. Breeze remains the
default application style and window decoration.

## What's in it

| Part | Path |
| --- | --- |
| Nobara global theme and splash | `usr/share/plasma/look-and-feel/org.nobaraproject.desktop` |
| Nobara Plasma style | `usr/share/plasma/desktoptheme/Nobara` |
| Nobara application colors | `usr/share/color-schemes/Nobara.colors` |
| Optional panel layout and Minimize All widget | `usr/share/plasma/layout-templates`, `usr/share/plasma/plasmoids` |
| Papirus-Dark icons with violet folders and Nobara branding | `usr/share/icons/Nobara`, `usr/share/icons/hicolor` |
| Nobara wallpapers, including Nobara Winds | `usr/share/wallpapers` |
| Plasma Login wallpaper | `usr/share/plasmalogin/wallpapers/nobara` |
| Nobara GTK 3/4 theme (current Breeze GTK under the Nobara name) | `usr/share/themes/Nobara` |
| Nobara Konsole profile and colors | `usr/share/konsole` |

Original Aurorae decoration artwork is retained in `usr/share/aurorae` for
later repair. **It is excluded from the installable package.** Plasma artwork
`_templates` are also source-only. GTK 2 and SDDM are not supported.

## What was fixed

Details and evidence are in [CHANGELOG.md](CHANGELOG.md) and [AUDIT.md](AUDIT.md).

- Explicit Breeze application style and corrected Plasma metadata/settings.
- Removed obsolete switcher defaults and unused Plasma 5 lockscreen files.
- Packaged Nobara Winds for Plasma's wallpaper discovery and default selection.
- Created an icon overlay that inherits Papirus-Dark, using violet folders and
  native small icons without modifying the installed Papirus theme.
- Fixed GTK dark imports to find the required system Breeze-Dark theme.
- Removed GTK 2 and its exclusive assets, plus an unused broken GTK template.
- Nobara's GTK 3/4 theme was an unmodified copy of Breeze GTK 5.27.6; it now
  imports the installed Breeze GTK, so it stays current with Plasma.
- Removed an invisible infinite splash animation that caused continuous redraws.
  The settled splash image is unchanged.
- Removed hidden setup commands and distribution-wide configuration changes.

The original main GTK stylesheets, retained artwork and palettes are preserved.
Konsole's ANSI black still matches its background, as it does upstream.

## Install on Arch Linux

A local package recipe is included as **`plasma6-themes-nobara-fixed`**,
version `0.2.0-1`. Download the source and prebuilt Arch package from
[release v0.2.0](https://github.com/orlfman/nobara-plasma-6.8/releases/tag/v0.2.0).
Install from the AUR as
[plasma6-themes-nobara-fixed](https://aur.archlinux.org/packages/plasma6-themes-nobara-fixed),
matching the naming of the Vapor package. With an AUR helper such as paru:

```sh
paru -S plasma6-themes-nobara-fixed
```

Or build the AUR recipe manually:

```sh
git clone https://aur.archlinux.org/plasma6-themes-nobara-fixed.git
cd plasma6-themes-nobara-fixed
makepkg -si
```

To build the pinned GitHub release directly, with the dependencies below installed:

```sh
git clone --branch v0.2.0 https://github.com/orlfman/nobara-plasma-6.8.git
cd nobara-plasma-6.8
(cd packaging && makepkg --cleanbuild --clean)
sudo pacman -U packaging/plasma6-themes-nobara-fixed-0.2.0-1-any.pkg.tar.zst
```

Building requires Arch's `base-devel` tools and Python. Required runtime packages:

- `plasma-workspace>=6.8` and `plasma-desktop>=6.8`
- `breeze>=6.8`, `breeze-cursors>=6.8` and `breeze-gtk>=6.8`
- **`papirus-icon-theme>=20260801`** — required, not optional

Optional consumers are `konsole` and `plasma-login-manager`. Papirus supplies
the icon artwork; Breeze GTK supplies the GTK 3/4 theme.

The package installs appearance resources and documentation system-wide. It
does not select a theme, replace your panel, synchronize login settings or
change screen locking/authentication. Avoid copying the entire source tree
into `/usr`, because it contains the unrepaired Aurorae files.

The release includes `SHA256SUMS` for its source, Arch package and build recipe.
For a development snapshot, run `python3 -I tools/prepare-package.py` first.

See [PACKAGING.md](PACKAGING.md) for package checks, removal instructions,
reviewed packaging warnings and the later AUR publication requirements.

## Select the appearance

In **System Settings > Colors & Themes > Global Theme**, select **Nobara**.
It selects Breeze widgets/decorations, Nobara colors, Plasma style, icons and
splash. Choose the supplied desktop layout only if you want its panel layout.
The wallpaper default does not forcibly replace an existing wallpaper choice.

Icons can also be selected independently as **Nobara**. They inherit
Papirus-Dark; folder colors and branding are overridden without recoloring or
rewriting Papirus. See [ICONS.md](ICONS.md).

Select the GTK theme through Plasma's GTK appearance settings. Nobara's GTK
theme was always Breeze GTK (an unmodified 5.27.6 copy upstream); it now loads
the installed Breeze and Breeze-Dark, so choosing **Nobara** or **Breeze** looks
the same. GTK apps get Nobara's colors from Plasma's active color scheme, either
way. No global dark preference is forced. Apps that ignore GTK themes may differ.

In Konsole, select the **Nobara** profile or just its color scheme in your own
profile to keep your current font and terminal preferences.

### Plasma Login

Only **Plasma Login Manager** is supported. This project provides appearance
assets and a wallpaper, using the login manager's built-in layout. It does not
provide replacement greeter QML or authentication configuration.

After system-wide installation, use **Apply Plasma Settings…** in Plasma Login's
settings, review the settings being copied, then select the wallpaper separately.
See [PLASMA-LOGIN.md](PLASMA-LOGIN.md) for the full procedure and testing limits.
A theme installed only in your home folder cannot serve the separate login account.

## Checks and compatibility

Validated on Plasma 6.8.2, Qt 6.12 and Papirus 20260801. Structural/GTK/QML checks,
icon inheritance, isolated widget/splash regressions and extracted-package KDE
loading pass. Live desktop/login appearance, monitor/accessibility behavior and
GPU performance still need validation. See [PERFORMANCE.md](PERFORMANCE.md).

```sh
tools/check.sh
python3 -I tools/test-icon-builder.py
tools/check-runtime.sh
```

The runtime checks need a developer compiler and Qt development tools. See
[AGENTS.md](AGENTS.md) for the full check environment and
[CONTRIBUTING.md](https://github.com/orlfman/nobara-plasma-6.8/blob/main/CONTRIBUTING.md)
for reporting problems or proposing changes.

## License and credits

Theme files and artwork come from Nobara and their respective KDE/upstream
authors. See [SOURCE.txt](SOURCE.txt), [LICENSE](LICENSE), file-level notices and
[UPSTREAM-NOTICES.md](UPSTREAM-NOTICES.md) for provenance and the original
GPL/LGPL declarations. Papirus artwork is supplied by its required dependency,
not bundled in this repository.

Nobara names and logos belong to their respective owners. This is an unofficial
adaptation, not affiliated with or endorsed by the Nobara Project.
