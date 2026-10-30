# nobara-6-8-3: plan

Status (2026-10-29): v0.2.0 (GTK wrapper) released on GitHub and AUR. User-facing steps 1–5 and the runtime/performance audit
are complete. Local Arch package plasma6-themes-nobara-fixed 0.1.0-1 builds and
passes exact-payload, KDE loader and existing structural/runtime checks. The
binary excludes unrepaired Aurorae and source templates, retained in the source
archive. Public source repository: https://github.com/orlfman/nobara-plasma-6.8.
Stages 1–5 and GitHub setup are recorded in the initial adaptation commit.
GitHub release v0.1.0 provides source and an Arch package. AUR package plasma6-themes-nobara-fixed 0.1.0-1 is submitted; no installation; live visual/login/GPU testing
and optional Aurorae repair remain deferred.

In progress: nobody.

Agents: read `AGENTS.md` first (shared rules, turn-taking, checks).

## Goal and approved scope

User instruction, 2026-10-29: "just the kde plasma theme, wallpapers, login theme,
and icons"; "only plasmalogin". Keep Nobara's look while fixing compatibility
with Plasma 6.8.2. Classic Breeze remains the default widget style; Union is
user-selected. The user also explicitly confirmed keeping the Konsole theme
and GTK themes on 2026-10-29, then clarified during step 4 that GTK 2 must
be dropped: keep GTK 3/4 only. Publishing only when the user asks.

Keep:

- Global theme, Nobara Plasma style, application color scheme, and splash.
- Nobara wallpapers, packaged so they work in Plasma's wallpaper chooser.
- The three original Nobara hicolor icons and the Nobara icon theme inheriting
  Papirus-Dark with violet folders, without modifying Papirus.
- The visual panel layout and Peek at Desktop widget, after removing the hidden
  command-running widget. Applying a layout must remain an explicit user choice.
- Plasma Login appearance support using the wallpaper and system-wide theme
  assets with the login manager's existing appearance settings.
- Breeze window decoration, as selected by the global theme.
- Existing Nobara Aurorae artwork: retain for later repair as an optional
  appearance choice. Do not enable it by default.
- Nobara Konsole profile and color scheme (`usr/share/konsole/Nobara.profile`
  and `Nobara.colorscheme`).
- Nobara GTK 3/4 theme (`usr/share/themes/Nobara/`), as a wrapper importing
  the installed Breeze GTK (since 2026-10-29; upstream was a Breeze 5.27.6 copy).

Remove from the working payload when implementing:

- All `etc/` distro defaults (including screen-lock, font, pointer, GTK defaults).
- Nobara's polkit action, hidden run-command widget, apply/clean scripts,
  systemd units and presets. Remove the hidden widget from the panel layout too.
- SDDM theme and all SDDM-specific support.
- GTK 2 theme and the assets used only by it (user decision during step 4).
- Unused global-theme lockscreen files and legacy/backup files after preserving
  any live settings they supply. Keep the Aurorae decoration for later work.

Do not remove the repository LICENSE, attributions, SOURCE.txt, documentation,
or source artwork that the remaining theme actually uses. Additional terminal
themes such as Alacritty are outside the current scope.

## Plasma Login findings and approach

Reviewed KDE's plasma-login-manager at tag `v6.8.2` and the installed package
`plasma-login-manager 6.8.2-1` on 2026-10-29.

- Nobara's imported `usr/share/plasmalogin/` contains only
  `wallpapers/nobara/nobara-winds1.webp`. It does not contain a custom greeter.
- Plasma Login loads a built-in QML greeter. Its System Settings page provides
  "Apply Plasma Settings…" for colors, Plasma theme, cursor, fonts and other
  desktop settings, plus a separate wallpaper selector.
- Theme resources must be installed system-wide for the greeter account to
  access them; a desktop-only install in the user's home is insufficient.
- Plan: reuse the installed Nobara color scheme/Plasma style/icons and default
  wallpaper through the existing login appearance settings. Document activation
  as an explicit user action. Do not overwrite Plasma Login's greeter files,
  authentication, service configuration, or `/etc/plasmalogin.conf` on install.
- A custom greeter layout is outside this asset-only approach. If later requested,
  first assess it as a separate change to Plasma Login itself.

## Earlier decisions, resolved by the scope instruction

- **D1: resolved.** Remove Nobara's passwordless polkit action. No automatic
  invocation of papirus-folders or global recoloring of Papirus during install.
- **D2: resolved.** Remove hidden command widget, scripts, units, and presets.
- **D3: resolved.** Keep Nobara GTK 3/4; drop GTK 2 (user clarified during
  step 4, 2026-10-29).
  Step 2 review found the main GTK 3/4 stylesheets are light and the dark variants
  explicitly import Breeze-Dark. Preserve both. Fixed dark imports to use the
  system-wide provider so per-user installs work; require `breeze-gtk` in any
  future package. No global GTK preferences or colors are changed.
  2026-10-29 (user: "do it"): the main stylesheets proved to be a byte-identical
  Breeze GTK 5.27.6 copy (all 167 assets too). Replaced with imports of the
  installed Breeze GTK; renders pixel-identical to stock Breeze. Released 0.2.0.
- **D4: resolved.** Remove the distro `etc/` defaults.
- **D5: preserve upstream appearance for now.** Blue Plasma accents vs purple
  application accents are a visual choice, not an approved restyle. No need to
  block cleanup on it; ask before changing those colors.
- **D6: resolved by user, 2026-10-29.** Retain the Aurorae decoration files.
  Repair and test them later as an optional appearance choice. Breeze remains
  the default window decoration. Do not install the broken flat layout as-is.
- **D7: resolved.** Plasma Login only; remove SDDM.
- **D8: partially resolved.** Keep the Nobara Konsole theme (user confirmed
  2026-10-29). No Alacritty theme requested. The stage-5 local working package name is
  plasma6-themes-nobara-fixed; public repository is orlfman/nobara-plasma-6.8;
  v0.1.0 and AUR 0.1.0-1 are published; later releases/updates require a request.

## Icons: implemented in step 3

The global theme now selects `Theme=Nobara`. `usr/share/icons/Nobara` inherits
Papirus-Dark and supplies violet folders via links to the installed artwork,
with alias/high-DPI coverage and unchanged native 16px forms. Three relative
links reference the original hicolor branding. No Papirus files are modified.
Generated against `papirus-icon-theme 20260801-1`: 1,705 links, all resolving.
See ICONS.md; regenerate with `tools/build-icons.py --build`, check with `--check`.

User decision (2026-10-29): **require `papirus-icon-theme`** in the
package's `depends` (not `optdepends`). Do not bundle the full icon set.
Required compatibility dependency: `breeze-gtk`, supplying the whole
GTK 3/4 theme through the wrapper imports. Both are required by the local PKGBUILD and documented in PACKAGING.md.

Plasma Login activation is documented in PLASMA-LOGIN.md. Use system-wide assets
and the existing settings module; do not install config files or privileged
custom helpers. The mock greeter was checked offscreen; live activation remains
an explicit user action after installation.

## Order of work

1. Done: original import + initial audit, then record the user's visual-only
   scope and check Plasma Login's supported appearance path.
2. Done 2026-10-29: scope cleanup (user-facing step 1). Removed 42 files from
   the excluded components and the hidden widget entry from the panel layout.
   `tools/check.sh` now checks the retained scope and removed helper references.
3. Done 2026-10-29 (user-facing step 2): explicit `widgetStyle=Breeze`, removed
   stale switcher/dead splash/breezerc sections, migrated effect settings into
   `plasmarc`, corrected Plasma-style ID and internal color scheme name, preserved
   metadata notices, packaged the Nobara Winds default wallpaper, and removed
   confirmed-unused backup/splash files plus the empty `.codex`. GTK dark imports
   now work from either installation layout using required `breeze-gtk`.
   All checks pass; artwork/colors, Konsole and Aurorae remain preserved.
4. Done 2026-10-29 (user-facing step 3): generated the Nobara icon theme,
   verified icon aliases/inheritance/rendering in isolated system-search and
   per-user layouts, documented login activation, and smoke-tested the stock
   mock greeter offscreen. Real login-account appearance needs a later live test.
5. Done 2026-10-29 (user-facing step 4): full audit. Fixed icon-builder failed
   publication handling, enforced QML/JS syntax, removed GTK 2 (12 files + 99
   exclusive PNGs) per user instruction, and removed an unused GTK decoration
   template whose 24 SVG targets never existed. Final checks/regressions pass;
   see AUDIT.md for evidence and remaining live-testing limits.
   Follow-up runtime/performance audit: removed a measured invisible splash
   animation, verified unchanged settled pixels and controller behavior, and
   measured icon overhead. See PERFORMANCE.md and latest AUDIT.md entry.
6. Done 2026-10-29 (user-facing stage 5): local Arch packaging. Added explicit
   install manifest, PKGBUILD/.SRCINFO, deterministic source snapshot/checksum
   helper and exact archive validator. Built plasma6-themes-nobara-fixed 0.1.0-1:
   1,950 files/links, 1,705 intact icon links; Aurorae/_templates excluded from
   installation but retained in source. KDE extracted-package probes and all
   source/runtime checks pass. namcap has no errors; ten warnings reviewed.
   PACKAGING.md covers build, dependencies, installation/removal, remaining live
   checks and requirements before any later publication. No installation.
7. Done 2026-10-29: GTK 3/4 wrapper over the installed Breeze GTK (Claude
   Code). Source manifest 1,950 -> 1,783 files. Released as v0.2.0 (GitHub
   release + AUR 0.2.0-1) at the user's request.
8. Later optional work: repair/package the Aurorae decoration with its own
   theme directory and test it before offering installation.
9. Only on user request: install/apply, commit, create/push GitHub, publish to AUR.

## Current handoff

Steps 1–5 and the GitHub presentation/setup are committed on main. Public origin:
https://github.com/orlfman/nobara-plasma-6.8. README follows the Vapor project
structure; contribution guidance and a bug-report form are included. Original
import history and author/license notices are preserved. Generated source and
binary archives remain ignored by Git; v0.1.0 publishes them as release assets,
with the build recipe and checksums. AUR package plasma6-themes-nobara-fixed 0.1.0-1 is submitted.

The local package and source snapshot are in packaging/. Regenerate after
source/docs changes, rebuild and compare against the current tree. A release checkout
can build directly with makepkg using the pinned downloadable source. Development
snapshots use tools/prepare-package.py. Bump the version before publishing new
source; never overwrite a published release asset. AUR updates need
a separate request; clean-Arch validation remains pending. See PACKAGING.md.

Full structural/GTK/QML checks, four icon-builder recovery cases, isolated splash/
controller regressions and extracted-package KDE/icon probes pass. The package
contains GTK 3/4, Konsole, login wallpaper and Papirus overlay. GTK 2 and distro
integration are absent. Aurorae/_templates are source-only. Live KWin/session/
login authentication, monitor/accessibility behavior and live GPU performance
remain unvalidated. See AUDIT.md and PERFORMANCE.md for evidence and limits.
No system package installation or theme activation was requested.

AUR checkout: ../aur-plasma6-themes-nobara-fixed (master, SSH origin). Fresh
public-source build, checksum, full payload comparison and metadata checks pass;
namcap has zero errors and the ten previously reviewed warnings. Only the recipe
and .SRCINFO are published to AUR. GitHub main documentation now describes AUR;
v0.1.0 tag/assets remain unchanged. Compare published packages against the matching
release checkout, not later edited documentation on main.
