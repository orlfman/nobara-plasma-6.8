# nobara-6-8-3: audit findings

Audit: 2026-10-29 (America/Phoenix). Auditor: Claude Code (Claude Opus 5.5).
Audited: `kde-nobara` 6.7.5 as shipped, Nobara-Project/nobara-core-packages
commit `4794fa0c` (2026-10-18), imported unmodified as this repo's first commit.
Against: Plasma 6.8.2, KDE Frameworks 6.31, Qt 6.12, GTK 3.24 / GTK 4 on CachyOS.
Status: all findings open. Nothing has been changed yet.

Priorities: P1 = fix before shipping anything, P2 = real bug or wrong behavior,
P3 = cleanup, cosmetic, or dead code.

## Summary

| # | P | Finding |
| --- | --- | --- |
| 1 | P1 | polkit rule lets any user run `papirus-folders` as root with any arguments, no password |
| 2 | P2 | Hidden "Run Command" panel widget runs `nobara-apply-theme.sh` on every Plasma start |
| 3 | P2 | `nobara-apply-theme.sh` never finishes: `exec pkexec` ends the script, so it repeats every login |
| 4 | P2 | Global theme asks for widget style "Nobara", which doesn't exist; applying it never sets a style |
| 5 | P2 | Global theme sets a Plasma 5 window switcher name that Plasma 6 removed |
| 6 | P2 | `gtk-dark.css` imports Breeze-Dark, and Nobara forces dark, so Nobara's own GTK 3/4 CSS is bypassed |
| 7 | P2 | `etc/xdg/kscreenlockerrc` turns off automatic screen locking and lock on resume |
| 8 | P3 | Plasma style highlights in Breeze blue while the app colors use Nobara purple |
| 9 | P3 | Lock screen folder is never used by Plasma 6.8, and is an outdated copy anyway |
| 10 | P3 | Aurorae window decoration files are dumped flat into `aurorae/themes/`, so the theme can't load (also unused) |
| 11 | P3 | Logout systemd unit likely never runs (conflicts with `shutdown.target`) |
| 12 | P3 | Wallpaper only via a hardcoded path; Plasma style names a wallpaper package that doesn't exist |
| 13 | P3 | Dead lines in the global theme: `[KSplash]`, `[breezerc]` |
| 14 | P3 | Color scheme leftovers: no Header colors, `ColorScheme=MateriaDark` |
| 15 | P3 | Legacy Plasma 5 `metadata.desktop` files next to `metadata.json` |
| 16 | P3 | Unused files: splash images, panel SVG backup, `.codex` |

Checked and fine: see "Passed" at the end.

## 1. [P1] polkit rule: root without a password for any user

`usr/share/polkit-1/actions/org.nobara.theme.policy:14-18`

The action allows `/usr/bin/papirus-folders` through `pkexec` with
`allow_any`, `allow_inactive` and `allow_active` all `yes`. Any user, including
ones not at the machine (SSH, other seats), can run that program as root with
any arguments and no password. The rule doesn't restrict arguments; polkit
can't. `papirus-folders` is a shell script that rewrites symlinks under the
Papirus icon theme folders; I haven't checked whether its argument handling can
be abused to touch other paths, but a rule like this shouldn't depend on that.

Its only purpose is finding 3's one-time "make Papirus folders violet" step.

Suggested fix (user decides, PLAN.md D1): drop the rule. Options for the folder
color: ship it as an optdepend + README instruction (`papirus-folders -C violet
--theme Papirus-Dark`, run once by the user with sudo); or require
authentication (`auth_admin_keep`) and run it only from an explicit user action.

## 2. [P2] Hidden panel widget runs a script at every Plasma start

`usr/share/plasma/plasmoids/com.kde.plasma.nobara.runcommand/contents/ui/main.qml`
and the panel layout `usr/share/plasma/layout-templates/org.kde.plasma.desktop.nobaraPanel/contents/layout.js`.

The layout adds `com.kde.plasma.nobara.runcommand`, an invisible widget
(`visible: false`) whose only job is `Component.onCompleted:` run
`nobara-apply-theme.sh` through the Plasma5Support `executable` engine. Its
metadata calls it a "Butchered version of Run Command plasmoid". So every
Plasma start, on every panel created from this layout, runs the script, and
users can't see or easily find why. It also keeps a dependency on the
deprecated Plasma5Support executable engine.

Suggested fix: remove the widget from the layout and the package; if any
first-run step is kept, use a visible, one-shot mechanism (autostart entry that
deletes its own marker, or just documentation).

## 3. [P2] `nobara-apply-theme.sh` stops at `exec pkexec`

`usr/share/plasma/look-and-feel/org.nobaraproject.desktop/nobara-apply-theme.sh:9`

`exec` replaces the shell with `pkexec`, so nothing after line 9 runs: the
`breezerc` copy, the Papirus sed, and line 29 that writes the
`~/.config/nobara-theme-first-apply` marker. Without the marker, the "first
apply" check at line 6 passes again next time, so (with finding 2) the script
and `pkexec papirus-folders` run at every login. Also:

- The sed at line 24 replaces `Papirus-Dark` with `Papirus-Dark` (no-op), after
  grepping `~/.config` for a theme name, `papirus-colors-dark`, it never sets.
- Line 4 greps `~/.config/kdedefaults/plasmarc` without checking it exists
  (harmless error message on a fresh account).
- `gsettings set org.gnome.desktop.interface gtk-theme Nobara` duplicates what
  Plasma's GTK settings already do.

Suggested fix: goes away with D1/D2. If anything stays, drop `exec`, write the
marker, and delete the no-op sed.

## 4. [P2] `widgetStyle=Nobara` doesn't exist

`usr/share/plasma/look-and-feel/org.nobaraproject.desktop/contents/defaults:2`

No Qt style called "Nobara" exists in any Nobara repo or history; the line has
been there since the theme's first commit (January 2024). In 6.8.2,
`KLookAndFeelManager::setWidgetStyle()` (plasma-workspace
`libklookandfeel/klookandfeelmanager.cpp:186-208`) tries
`QStyleFactory::create(style)` and returns without writing anything when it
fails. So applying the Nobara global theme never sets the widget style: users
keep whatever they had. On a fresh Nobara that's Breeze, which the user
confirmed on a real Nobara 44 boot (2026-10-29). The style KCM shows the
"Application Style" part of the global theme as available although it does
nothing.

Fix: `widgetStyle=Breeze` (matches what Nobara actually shows).

## 5. [P2] Plasma 5 window switcher name

`.../contents/defaults:16-20`

`[kwinrc][WindowSwitcher] LayoutName=org.kde.breeze.desktop`: that switcher
was removed in Plasma 6. Applying the theme writes it to `kwinrc [TabBox]`,
overwriting the user's Alt+Tab choice; KWin 6.8.2 then logs "Could not load
window switcher package" and falls back to `thumbnail_grid`
(kwin `src/tabbox/tabboxhandler.cpp:169-175`). `[DesktopSwitcher]` is a
feature Plasma 6 removed and is ignored.

Fix: remove both sections (same fix as the Vapor project).

## 6. [P2] Nobara's GTK theme is mostly bypassed

`usr/share/themes/Nobara/gtk-3.0/gtk-dark.css:1`, `gtk-4.0/gtk-dark.css:1`,
`etc/xdg/gtk-3.0/settings.ini`, `etc/xdg/gtk-4.0/settings.ini`

Both `gtk-dark.css` files are a single
`@import url("../../Breeze-Dark/gtk-N.0/gtk.css")`. Nobara's settings set
`gtk-application-prefer-dark-theme=true`, so GTK loads `gtk-dark.css`, i.e.
Breeze-Dark, not Nobara's own 4,462-line `gtk-3.0/gtk.css` (or 4,045-line
`gtk-4.0/gtk.css`). Effects:

- GTK apps look like Breeze Dark (with KDE's color scheme colors injected by
  Plasma), not like the Nobara GTK theme.
- It depends on `breeze-gtk` being installed at `/usr/share/themes/Breeze-Dark`
  (relative import), and breaks if the theme is installed under
  `~/.local/share/themes`.

Needs the user's decision (D3): what Nobara GTK apps should look like. Ask them
to check a GTK 3 app on their Nobara 44 boot. Both `gtk.css` files themselves
parse with 0 errors.

## 7. [P2] Screen locking turned off in `etc/xdg/kscreenlockerrc`

`etc/xdg/kscreenlockerrc`: `Autolock=false`, `LockOnResume=false`.

These are distro defaults, not theme, and they lower security (no lock after
idle, no lock after sleep). Same for the other `etc/xdg` files: they set
system-wide defaults (fonts, cursor speed, `LookAndFeelPackage`, GTK settings),
which a theme package for other distros shouldn't ship.

Suggested fix (D4): leave `etc/` out of any package.

## 8. [P3] Plasma style uses Breeze blue, apps use Nobara purple

`usr/share/plasma/desktoptheme/Nobara/colors:51` (Selection `61,174,230`),
backgrounds pure black `0,0,0`; `usr/share/color-schemes/Nobara.colors`:
Selection `108,84,170` (purple), Window `18,18,18`, View `30,30,30`.

Panels, Kickoff and Plasma popups highlight in Breeze blue on black; apps
highlight in purple on dark grey. 148 values differ between the two files. It
may be intentional (black panel look); the blue selection looks like a Breeze
leftover. User decides (D5) after looking at Nobara 44.

## 9. [P3] Lock screen folder: unused and outdated

`usr/share/plasma/look-and-feel/org.nobaraproject.desktop/contents/lockscreen/`

kscreenlocker 6.8.2 loads the lock screen only from the Plasma shell package
(`greeter/greeterapp.cpp:502-516` → `Plasma/Shell`, `org.kde.plasma.desktop`;
the shell package's fallback is another shell, libplasma
`shellpackage.cpp:72-87`). A global theme's `lockscreen/` folder is never read.
It's also an older fork of Plasma's lock screen: versioned imports, no
`PasswordSync`/`qmldir`, and `LockOsd.qml:10` imports `"../osd"`, which doesn't
exist in this package (qmllint: import error + 5 unresolved aliases).

Fix: delete the folder (`config.qml`, `config.xml` included).

## 10. [P3] Aurorae decoration files in the wrong place

`usr/share/aurorae/themes/` holds `decoration.svg`, the button SVGs,
`metadata.desktop` and `Nobara` (the theme's rc file) directly. Aurorae needs
`aurorae/themes/Nobara/` with `metadata.desktop`, `decoration.svg`, buttons and
`Nobararc`. As shipped, no "Nobara" decoration can load, and the files would
clash with any other package doing the same. The global theme uses the Breeze
decoration anyway (`defaults:22-23`).

Fix (D6): delete it, or move it into a proper `Nobara/` folder if the user
wants it as an optional decoration. Metadata says it's by Vince Liuice
(WhiteSur/Orchis author), GPL v3.

## 11. [P3] Logout unit likely never runs

`usr/lib/systemd/user/nobara-clean-theme-logout.service:3,10`

`WantedBy=shutdown.target` + `Before=shutdown.target` with default
dependencies, which add `Conflicts=shutdown.target`: when the user manager
stops, `shutdown.target` pulls in a unit that conflicts with it. Usually needs
`DefaultDependencies=no`. Not verified at runtime. The login unit runs the same
cleanup script anyway, and the cleanup only matters for finding 3's marker.
`nobara-clean-theme.service` has no `[Install]` and nothing enables it.

Fix: goes away with D2; otherwise drop the logout unit.

## 12. [P3] Wallpaper

- `contents/plasmoidsetupscripts/org.kde.plasma.folder.js:3` hardcodes
  `/usr/share/wallpapers/nobara-winds1.webp` (breaks for user installs).
- No `[Wallpaper] Image=` in `defaults`, and all wallpapers are loose image
  files, not wallpaper packages.
- `desktoptheme/Nobara/metadata.desktop:22`: `defaultWallpaperTheme=Nobara`,
  a wallpaper package that doesn't exist, so Plasma falls back to `Next`.

Fix: same as Vapor: make `nobara-winds1` a wallpaper package, set
`[Wallpaper] Image=` in `defaults`, drop the folder script.

## 13. [P3] Dead lines in the global theme

`.../contents/defaults`

- `:28-29` `[KSplash] Theme=org.nobaraproject`: 6.8.2 reads
  `[ksplashrc][KSplash]` (klookandfeelmanager.cpp:537-545), and the ID is
  wrong too. Harmless: Plasma uses the package's own splash
  (`org.nobaraproject.desktop`), which is what `etc/xdg/ksplashrc` also says.
- `:25-26` `[breezerc][Common]`: the look-and-feel manager doesn't apply
  `breezerc` at all (that's why the script copies it).

Fix: remove both.

## 14. [P3] Color scheme leftovers

`usr/share/color-schemes/Nobara.colors`: no `[Colors:Header]` groups (KDE
falls back to Window colors, no visible effect); `[General]
ColorScheme=MateriaDark:106` (internal name left from the scheme it was based
on).

## 15. [P3] Legacy metadata files

`metadata.desktop` next to `metadata.json` in the global theme, the Plasma
style and the run-command widget. Plasma 6 reads the JSON; the global theme's
`.desktop` even has `X-KDE-PluginInfo-License` twice. Exception: the Plasma
style's `metadata.desktop` still supplies `[ContrastEffect]`,
`[AdaptiveTransparency]` and `[Wallpaper]` (libplasma `theme_p.cpp:31-40`
reads it when there's no `plasmarc`). Fix: move those three groups into a
`plasmarc` file (as stock Breeze does), then delete the `.desktop` files.

## 16. [P3] Unused files

- `contents/splash/images/busywidget.svgz`, `fedora-logo-sprite_classic.svg`:
  `Splash.qml` uses neither (its logo line is commented out).
- `desktoptheme/Nobara/widgets/panel-background_backup.svgz`.
- `.codex` (empty file from Nobara's repo; could also get in the way of a
  Codex `.codex/` project folder).

## Passed

- All JSON metadata parses; all `.svgz` are valid gzip.
- Splash: 1 qmllint warning (unqualified `stage`), same kind as stock.
- SDDM theme: Qt 6 (`QtVersion=6`, `Theme-API=2.0`), based on Plasma's Breeze
  SDDM theme; qmllint warnings per file equal stock 6.8.2's
  (10/11/24/69/8). Needs `qt6-5compat` (`Qt5Compat.GraphicalEffects`) and
  plasma-workspace's `org.kde.breeze.components`. Not run (no sddm here).
- Panel layout: same as Plasma 6.8.2's default panel plus the two Nobara
  widgets; every stock widget ID exists in 6.8.2.
- Peek at Desktop fork (`org.kde.plasma.nobara.showdesktop`): Plasma 6 API,
  warnings are qmllint's usual context gaps.
- Plasma setup scripts (kickoff icon `nobara-app-menu-icon`, systray
  `scaleIconsToFit`): keys exist in 6.8.2; icon is shipped in hicolor.
- GTK: `gtk-3.0/gtk.css` and `gtk-4.0/gtk.css` parse with 0 errors;
  `window_decorations.css` assets exist.
- Konsole profile and color scheme: fine.

## Testing limits

- Nothing was run in a live Plasma session; the theme was not applied.
- `sddm`, `papirus-icon-theme` and `papirus-folders` aren't installed here.
- Findings 2, 3 and 11 are from reading code; not executed (they call pkexec).
- Behavior on Nobara 44 itself only through the user's report (widget style).
