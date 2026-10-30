# nobara-6-8-3: audit findings

Audit: 2026-10-29 (America/Phoenix). Auditor: Claude Code (Claude Opus 5.5).
Audited: `kde-nobara` 6.7.5 as shipped, Nobara-Project/nobara-core-packages
commit `4794fa0c` (2026-10-18), imported unmodified as this repo's first commit.
Against: Plasma 6.8.2, KDE Frameworks 6.31, Qt 6.12, GTK 3.24 / GTK 4 on CachyOS.
Status: steps 1–5 implemented; local packaging prepared; source published on GitHub; GTK 2 removed by user instruction. Findings 1–7, 9, 11–16 are
addressed by cleanup/compatibility fixes or documented behavior. Finding 8 is
preserved as an appearance choice; finding 10 is deferred for optional Aurorae
repair. Read the newest review for the evidence, dependencies and testing limits;
original findings remain below as historical records.

Priorities: P1 = fix before shipping anything, P2 = real bug or wrong behavior,
P3 = cleanup, cosmetic, or dead code.

## 2026-10-29: v0.1.0 release verification — Codex (GPT-6)

Reviewed release preparation on parent HEAD `6323ed5`. No new theme/runtime
changes: only source URL, packaging/release instructions and handoff records.

- Full tools/check.sh passes: scope/manifest, metadata/defaults, SVG integrity,
  all 1,705 icon links, all four GTK CSS files, KDE discovery and QML/JS syntax.
- The old package correctly failed current-tree comparison after release docs
  changed; regenerated source and rebuilt it to include those exact documents.
- Version 0.1.0 source is pinned to its GitHub release asset with a real SHA-256;
  .SRCINFO is generated from that recipe. Built archive verification covers all
  1,950 payload files/links, exact bytes, ownership/modes, deps and exclusions.
- Release assets include source, Arch binary package, PKGBUILD, .SRCINFO and
  SHA256SUMS. Tag points to the release-preparation commit; generated archives
  stay outside Git. Source-only Aurorae/templates remain preserved.
- No new findings. Previous runtime measurements/probes and reviewed namcap
  warnings still apply; live desktop/login/GPU checks and clean-Arch build
  validation remain pending. GitHub release does not imply AUR publication.

## 2026-10-29: GitHub setup and pre-push review — Codex (GPT-6)

Reviewed the uncommitted adaptation on HEAD `763b169` before its initial GitHub
commit/push, explicitly requested by the user along with Vapor-style repo setup.

- Confirmed authenticated account orlfman and created public
  https://github.com/orlfman/nobara-plasma-6.8. Repository description/topics and
  standard Issues/Projects/Wiki enabled. No tagged release or AUR upload.
- Upload candidates contained no credential/private-key pattern matches and no
  file above GitHub's 50 MiB warning threshold. Generated archives/build outputs
  are ignored. Original import history, license and provenance are preserved.
- Full tools/check.sh passes again: exact source install scope, metadata/defaults,
  compressed SVGs, all 1,705 icon links, all four GTK CSS parsers, Plasma listing,
  and QML/JS syntax. Context-dependent lint warnings remain as documented.
- Public README matches the Vapor project's structure but documents Nobara's
  own dependency, login and deferred-Aurorae constraints. Added contribution and
  bug-report guidance. Packaging remains local-source-based; the public README
  instructs fresh clones to generate the source archive before building.
- Changes in this publication pass affect documentation, project metadata and
  source snapshot contents only. Stage-5 runtime test results still apply.
  Regenerated the local package so its docs/checksum match the published tree.

No new theme defects found. Existing live desktop/login, GPU and clean-Arch
build limits remain. No user/session settings or installed files were changed.

## 2026-10-29: stage 5 local Arch packaging audit — Codex (GPT-6)

Audited the uncommitted working tree on HEAD `763b169`; this stage was explicitly
authorized as local packaging/preparation, without installation or publication.

- Added local `plasma6-themes-nobara-fixed 0.1.0-1`, architecture `any`, an explicit
  installation manifest, `.SRCINFO`, deterministic checksummed source snapshot
  helper and built-archive checker. No invented GitHub release URL or skipped
  source checksum. This local source recipe needs a public pinned release before
  any later AUR publication; the working package name is not an AUR reservation.
- The package contains only the retained appearance assets, notices and user
  documentation: 1,950 files/links including all 1,705 original overlay links.
  Byte-for-byte/source-link comparison, modes, root ownership, required package
  metadata and exact allowlist match pass. No `.INSTALL`, `/etc`, custom polkit,
  service/defaults, GTK 2, SDDM, Aurorae or artwork-template payload is included.
  Unrepaired Aurorae and `_templates` are preserved in the source archive/repo.
- Added required Plasma Workspace/Desktop, Breeze, Breeze cursors, Breeze GTK
  and Papirus dependencies. Breeze cursors is a separate installed package:
  verified `/usr/share/icons/breeze_cursors/index.theme` ownership rather than
  assuming Breeze contains it. Optional consumers: Konsole and Plasma Login.
  The Papirus minimum is the version used to generate/test the external links.
- `makepkg --cleanbuild --clean` verifies the real SHA-256, source manifest,
  defaults/CSS references and all Papirus targets, then builds successfully.
  Normal packaging tooling runs without installing or fetching dependencies.
- `namcap` reports **zero errors and ten reviewed warnings**. Five are QML/icon
  dependencies guaranteed transitively by Plasma/Papirus; five label appearance
  dependencies potentially unused because it cannot infer these data references.
  Checked widget/decoration/cursor ownership, panel applets, Breeze-Dark imports
  and all external Papirus links; retained the intentional dependencies.
- No existing non-directory install path was found on this machine (1,950
  candidate paths checked). This only describes the audited host, not all systems.
- Extracted the first successful package under `/tmp/nobara-stage5-n6m3c85b` and
  tested with all XDG settings/cache/data/state/runtime isolated, offscreen Qt and
  a disconnected session bus. KDE package/config/image/Plasma-theme loading
  passes, as do 96 icon size/scale cases, branding rendering and login/action
  fallback. The probes assert resources come from the extracted package.
- Existing full structural/GTK/QML checks and four icon-builder regression
  cases pass. Isolated controller QtTest: 6 passes (four behavior cases plus
  setup/cleanup). Splash regression: 0 frames/animation ticks, 0.041 ms CPU over
  3,046 ms; software/offscreen only. No changes to retained theme artwork/palette.
- Added build/install/removal instructions and updated login activation status.
  Installation is explicit; package installation neither applies the theme nor
  synchronizes login settings. Before removal, select alternatives and replace
  the custom panel widget if used. Normal distro icon-cache hooks are reused.

Limits: this is a local CachyOS build, not a clean Arch build or an AUR upload.
No system package installation, live KWin/login authentication, monitor or
accessibility validation, theme activation, commit, remote creation or push.
Live checks and optional Aurorae repair remain deferred. Rebuild after any
source/docs edits so the archive and its generated checksum remain current.

## 2026-10-29: bugs, runtime performance and Plasma 6.8.2 audit — Codex (GPT-6)

Reviewed uncommitted working tree on HEAD `763b169`. Installed versions confirmed:
Plasma Workspace/Desktop/libplasma/Breeze 6.8.2, Plasma Login 6.8.2, Qt 6.12.0,
Papirus 20260801-1. User requested a bug/performance/compatibility audit.

**Finding [P3 performance, fixed]: splash repeatedly animates an empty Image.**
`contents/splash/Splash.qml` had an unconditional ParallelAnimation containing
an infinite scale loop, but the logo source is commented out. An isolated
1280x800 software-rendered QQuickView, after intro completion, recorded 567 frame
swaps / 567 animation ticks and 40.801 ms CPU in 2,976 ms of observation. Removed
only the unused animation, keeping the positioning Image and all visible splash
artwork/geometry/transitions. Qualified the progress binding as root.stage.

After the fix, the same test recorded 0 frame swaps / 0 animation ticks and
0.038 ms CPU in 2,923 ms. Separate settled stage-4 before/after captures are
pixel-identical. This confirms a visible-equivalent idle-work reduction in the
offscreen software test, not a live compositor/GPU benchmark.

Added `tools/check-splash-idle.cpp` and `tools/check-runtime.sh` for the idle
regression (allowing up to two incidental frames after settling). Added actual
controller tests under tools/qml-tests with an org.kde.taskmanager test double:
activity/desktop filtering and restore, manually restored/closed windows,
focus changes, empty tasks and desktop-state switching. Tests assert the mock
before calling actions, so no real windows are minimized/restored. QtTest reports
six passes (four behavioral cases plus init/cleanup). The controller algorithm
matches upstream KDE plasma-desktop v6.8.2; source differences are versioned
imports and callback qualification. The custom Minimize All choice is preserved.

Icon performance, five alternating runs per theme with fresh isolated process
settings/caches, no filesystem-cache flush: 32 initial KIconLoader requests
(eight icons at four sizes) followed by 20,000 cached 32px requests. Medians:

| Theme | Initial requests | Cached requests | Peak RSS |
| --- | --- | --- | --- |
| Nobara | 18.836 ms | 11.090 ms | 37,712 KiB |
| Papirus-Dark | 18.308 ms | 10.953 ms | 37,728 KiB |

No material cached-cost or memory difference in this workload. Initial lookup
has a small measured difference; these numbers do not benchmark application or
whole-session startup. No icon changes were justified by this measurement.

Other findings/checks:

- No additional runtime compatibility blockers found in tested components.
- Runtime Plasma SVGs have no filter/Gaussian-blur chains. Internal gradient,
  clip and href IDs resolve (including authored templates). This is structural
  complexity evidence, not proof of compositor performance.
- The drag-hover timer is one-shot and event-triggered. The controller uses the
  standard event-driven tasks model; no custom polling or external commands.
- tools/check.sh: ALL CHECKS PASSED, including QML/JS syntax, metadata, effects,
  wallpaper, GTK 3/4 parsing/assets and all 1,705 icon links. Splash qmllint is now
  0 warnings (stock 1); remaining widget warning counts unchanged.
- Four icon-builder regression tests pass; shell syntax and git diff checks pass.
- Current-tree KDE package/config/image/theme probe and 96-case icon lookup/
  rendering probe pass again. Intro/progress behavior remains intact in rendering.
- PERFORMANCE.md records the measurements, reproduction commands and limits.
  README, agent guide, plan and changelog are updated. No palette restyling.

Limits: no actual KWin window integration, full installed Plasma session,
actual login authentication or live multi-monitor/accessibility/GPU tests.
The previous mock-greeter smoke tests remain evidence of resource loading only.
Aurorae remains preserved/deferred and must not be installed as-is. No package
installation, desktop/login settings changes, commit or push. All work remains
uncommitted. Compatibility is supported by these checks, not an unconditional
claim for every deployment configuration.

## 2026-10-29: step 4 assembled-theme audit — Codex (GPT-6)

Audited the uncommitted working tree on HEAD `763b169`, with `fd32ac5` as the
original-import baseline. The user authorized the audit/fixes and, during the
audit, explicitly instructed dropping GTK 2. No installation or user/session
configuration changes were made.

### Findings and actions

1. **[P2, fixed] Failed icon rebuild could replace the previous output.**
   tools/build-icons.py originally published before checking whether branding
   targets existed. Reproduced in a disposable project copy: deleting a required
   branding input made --build exit 1, but the previous index had already been
   overwritten. Added dependency validation before replacement, rollback on
   publish failure, and backup preservation if rollback itself fails. Added four
   regression tests in tools/test-icon-builder.py covering missing input,
   publication failure, rollback failure and a successful rebuild. The original
   missing-input reproduction now preserves the previous overlay.
2. **[P3, fixed] QML warning counts did not enforce syntax validity.**
   tools/check.sh now separately runs qmllint with only explicit syntax/duplicate-ID
   categories enabled and errors enforced for every retained QML/JS file.
   Existing contextual warning counts remain informational. A malformed temporary
   QML file is rejected by the same options; all retained files pass.
3. **[P3, fixed] Unused GTK decoration template had 24 nonexistent SVG targets.**
   usr/share/themes/Nobara/window_decorations.css referenced close-normal.svg,
   maximize-normal.svg and related files never present in the import. Earlier
   checks did not cover this root-level CSS file. This corrects the original
   audit's inaccurate Passed statement that its assets existed. Neither retained
   GTK stylesheet imports it. KDE kde-gtk-config v6.8.2 uses only the Breeze
   template at themes/Breeze/window_decorations.css for its generated user CSS;
   Nobara's main CSS already draws buttons using existing breeze-*-symbolic.svg.
   Removed the unused broken copy, preserving actual GTK titlebar appearance.
   Expanded CSS reference checking to every remaining CSS file in the theme.
4. **[Scope update, done] GTK 2 removed at user request.**
   Removed gtk-2.0 (12 text files) and the 99 PNG assets referenced exclusively
   by GTK 2. Checked references from GTK 3/4 and the root CSS before deletion.
   The 167 remaining assets are unchanged. Updated scope/dependency/docs/checks
   to retain GTK 3/4 only. The older GTK 2 runtime/engine limitations below no
   longer apply to the current project.

### Validation

- Final tools/check.sh: **ALL CHECKS PASSED**, including excluded integration,
  retained resources, JSON, compressed SVG, settings/metadata, CSS references,
  all four GTK 3/4 CSS variants, Plasma package discovery, icon dependency/alias
  checks and enforced QML/JS syntax. Shell/Python syntax and git diff --check pass.
- Four icon-builder regression tests pass. Original failed-build reproduction
  was rechecked after the fix in the disposable copy and preserves old output.
- Final 176 retained raster images decode; 51 SVG/XML documents parse. No broken
  local SVG links or icon symlinks. All 1,705 generated icon links still resolve.
- KDE KIconLoader integration probe passes again on the current tree (96 folder
  size/scale/alias cases, branding rendering, login/action parent fallback).
  KDE package/config/image/Plasma-theme probe also passes on the current tree.
  Step 3 already tested per-user layouts and the stock greeter in mock mode;
  no new login rendering or authentication claims are made in this audit.
- KDE v6.8.2 ImageProxyModel/ImageFinder source confirms wallpaper discovery
  scans standard wallpapers directories for loose files alongside wallpaper
  packages. Both the Nobara Winds package and 24 loose wallpapers are supported.
- Original LICENSE and the two metadata records in UPSTREAM-NOTICES.md match
  the import. Selected 296 original retained files were hash-compared before
  the GTK 2 scope change; after it, every remaining GTK artwork/main stylesheet/
  settings file except the documented dark-import wrappers matches the import.
  Konsole, Aurorae, icons and Plasma Login assets were not modified by this audit.
- Removed helpers, polkit/systemd/SDDM settings remain absent. Panel/setup
  scripts contain only their retained layout/icon/tray behavior, no removed
  command invocations. Local Markdown links resolve.

### Preserved choices and remaining limits

- Nobara's blue Plasma accents vs purple app accents remain as requested.
- Konsole's original ANSI black equals its background. This is a palette choice,
  documented in README; no unrequested recoloring was applied.
- Aurorae's broken original layout remains preserved for optional later repair,
  and must not be installed as-is. Breeze remains the default decoration.
- Actual login-account appearance, wallpaper synchronization, authentication,
  multi-monitor/accessibility behavior and live desktop/GTK appearance still
  need testing after an authorized installation. No package has been built or
  installed for Nobara, and no commit/push was made.

No unresolved blocker from this assembled-theme audit remains beyond the
explicit deferred/visual-testing limits above. All work remains uncommitted.
Sources newly inspected: KDE plasma-workspace v6.8.2 imageproxymodel.cpp and
imagefinder.cpp; kde-gtk-config v6.8.2 kded/config_editor/custom_css.cpp and
kded/gtkconfig.cpp. Original audit entries below remain historical evidence.

## 2026-10-29: step 3 icons and Plasma Login verification — Codex (GPT-6)

Reviewed uncommitted working tree on `763b169`; the user authorized step 3.
Papirus is now installed: `papirus-icon-theme 20260801-1`. Plasma Login is
`6.8.2-1`. No installed icon or login settings were changed.

Implementation:

- Added generated `usr/share/icons/Nobara/index.theme` with
  `Inherits=Papirus-Dark`, matching source directory contexts, sizes and scales.
  The global theme now selects this Nobara overlay rather than plain Papirus-Dark.
- 1,705 symlinks: 1,702 reference installed Papirus artwork; three relative links
  reference the original Nobara hicolor icons. Full Papirus artwork is not bundled.
  Papirus remains a required dependency; no papirus-folders runtime dependency.
- Generator models the upstream helper's violet operation at sizes 22/24/32/48/64
  and follows aliases across indexed contexts. Extra alias coverage matters for
  names such as folder-downloads and inode-directory: inheritance alone would
  follow the unchanged parent's blue folder. High-DPI and large variants are
  covered, while source 16px monochrome forms remain native.
- Added tools/build-icons.py with --build and read-only --check. The generated
  overlay is recreated only within this project. Papirus upgrade/path drift and
  missing dependencies are detected by the check, now part of tools/check.sh.
- Added README.md, ICONS.md and PLASMA-LOGIN.md with dependencies and activation.
  Login appearance uses globally installed resources and the existing KCM;
  wallpaper selection is a separate action. The KCM's appearance sync also copies
  fonts, keyboard/display/locale preferences, so the docs tell users to review it.
- Confirmed from the 6.8.2 startup code that Plasma Login reconstructs kdedefaults
  from LookAndFeelPackage; theme defaults such as Icons/Theme need not already be
  explicit in the copied kdeglobals. No custom authentication/power/service code
  or configuration file is shipped by this step.

Validation:

- `tools/check.sh`: ALL CHECKS PASSED; shell syntax/diff checks pass. GTK and QML
  results remain unchanged from step 2.
- All 1,705 links resolve. Absolute targets are restricted to installed Papirus/
  Papirus-Dark paths; original branding SVGs are byte-identical to the import.
  The parent's observed folder/download/home links still select blue, confirming
  the separate overlay supplies violet without recoloring the source theme.
- Built an isolated KDE KIconLoader probe: 96 folder/alias cases spanning
  16/22/24/32/48/64/96/128 sizes at scales 1 and 2 resolve within Nobara; sizes
  >=22 resolve to violet files and native 16px forms are preserved. All three
  branding icons rasterize. Shutdown/reboot/suspend/login/search/terminal icons
  are found through parent inheritance.
- The icon probe passes with project data on XDG_DATA_DIRS and again with a
  copied per-user `.local/share` tree (symlinks preserved). The earlier KDE
  package/config/image/theme probe also passes on the new per-user copy.
- Stock `/usr/lib/plasma-login-greeter --test` ran offscreen for bounded five-second
  tests using the mock authenticator and temporary XDG config/data/cache/state/
  runtime locations. Both default and KDE platform-theme cases reported no QML
  or resource loading errors; the latter used Nobara's full palette and theme.
  Both ended at the timeout (124), as expected for a running greeter event loop.
- Confirmed the supplied login image matches the packaged default, and staged
  theme/image permissions allow access after system-wide installation.

Limits: this tests resource lookup/rendering and mock greeter loading. It does
not validate the real login account, actual authentication, appearance-sync
execution, wallpaper-process rendering, multi-monitor login, or accessibility.
No changes to the user's desktop or active display manager, and no installation.
GTK 2 and optional Aurorae limitations from step 2 remain. No new unresolved
step-3 findings. All changes remain uncommitted.

References read (never executed): upstream papirus-folders `change_color()`;
KDE plasma-login-manager v6.8.2 KCM sync/wallpaper, helper, greeter mock mode,
settings and startup global-theme reconstruction sources. See ICONS.md and
PLASMA-LOGIN.md for links.

## 2026-10-29: step 2 compatibility verification — Codex (GPT-6)

Audited the uncommitted working tree on `763b169`, with the initial payload at
`fd32ac5` as the artwork/config comparison baseline. The user authorized step 2.

Changes:

- Finding 4: changed the global theme to `widgetStyle=Breeze`.
- Findings 5/13: removed WindowSwitcher, DesktopSwitcher, the dead `[KSplash]`
  entry and the ignored `[breezerc][Common]` section. The theme's existing splash
  is still discoverable by its own package; no KWin or user preferences are forced.
- Finding 15: moved ContrastEffect, AdaptiveTransparency and Wallpaper settings
  from the Plasma style's legacy metadata into `plasmarc`; effect values are
  identical. Removed duplicate global/Plasma-style `metadata.desktop` files and
  reproduced their full original contents in UPSTREAM-NOTICES.md, including
  author/license information. Aurorae's metadata.desktop is retained.
- Additional metadata mismatch: the Plasma style incorrectly reused the global
  theme ID `org.nobaraproject.desktop`. Corrected it to `Nobara`, matching the
  style folder and `[plasmarc][Theme] name`. No other JSON metadata values changed.
- Finding 12: moved `nobara-winds1.webp` into the `Nobara` wallpaper package as
  `contents/images/3840x2160.webp`, with JSON metadata. Both the global default
  `[Wallpaper] Image=Nobara` and the style fallback now resolve to it. Updated
  the fallback suffix/dimensions to match WebP at 3840x2160. Removed the hardcoded
  folder setup script. It supplies a default; it does not force a replacement
  of an existing desktop wallpaper. Other 24 loose wallpapers remain available.
- Finding 14: internal application scheme name `MateriaDark` -> `Nobara`. Every
  palette value is unchanged. No Header groups added: KColorScheme's Window
  fallback is valid and preserves the intended colors.
- Finding 16: removed unused busywidget.svgz, fedora-logo-sprite_classic.svg,
  panel-background_backup.svgz and the empty `.codex` file. Retained the original
  splash QML, its active image, and authored SVG templates.
- Finding 6 clarified: the main Nobara GTK 3/4 stylesheets define a light
  palette; the dark variants explicitly choose Breeze-Dark. Preserve that
  behavior. Replaced relative sibling imports with
  `file:///usr/share/themes/Breeze-Dark/gtk-{3,4}.0/gtk.css`, which works from
  either installation layout. **`breeze-gtk` is now a documented required
  dependency**, alongside required `papirus-icon-theme`. No forced GTK setting
  was restored, and no stylesheet artwork was replaced.

Validation:

- `tools/check.sh`: **ALL CHECKS PASSED**. Both main and dark GTK 3/4 CSS parse
  with zero errors; metadata, compressed SVG, retained scope, asset references
  and package discovery pass. `bash -n` and `git diff --check`: pass.
- Added read-only `tools/check-theme.py` to cover nested defaults, migrated
  settings, metadata IDs, default wallpaper, removed stale files and CSS paths.
- Built a small package probe in a scratch directory against the installed KDE
  libraries. CMake initially lacked ECM; direct compilation against the existing
  libraries succeeded without installing anything. With an offscreen GUI and
  isolated XDG config/data/cache/runtime directories, the probe verified:
  - global theme resolves to the test tree and exposes its splash;
  - KConfig sees nested `widgetStyle=Breeze` and no stale switcher;
  - Wallpaper/Images package is valid, has ID Nobara and a readable 3840x2160
    WebP found through the same QStandardPaths lookup as KDE's default helper;
  - Plasma style metadata ID, fallback wallpaper, contrast and adaptive
    transparency settings resolve correctly.
- Probe passed with the repo resources on XDG_DATA_DIRS, then again with a
  copied per-user `.local/share` layout on XDG_DATA_HOME. Both GTK dark variants
  also parsed with zero errors from that copied layout.
- Hash comparison: packaged wallpaper, Plasma Login image and splash image
  are all byte-identical to the original winds wallpaper. Main GTK CSS/assets,
  Konsole, Aurorae, custom icons and Peek at Desktop remain unchanged. Compared
  migrated effect settings and palettes against the import: values preserved.
- QML warning counts remain splash 1 (stock 1), Peek at Desktop 13/0/3. These
  context/qualification warnings were not turned into false runtime failures.

Sources inspected at KDE tag `v6.8.2`: plasma-workspace's
`libklookandfeel/klookandfeelmanager.cpp`, `wallpapers/defaultwallpaper.cpp`,
`shell/packageplugins/wallpaperimages/wallpaperpackage.cpp`, and libplasma's
`src/plasma/private/theme_p.cpp`.

Limits: package/config/image loading was exercised, but QML interfaces were not
rendered, no live session or login settings changed, and no package was installed.
GTK 2 rendering and engine dependencies remain untested. Future packaging must
include `breeze-gtk` and `papirus-icon-theme`. Papirus overlay work, Plasma Login
live appearance and optional Aurorae repair remain later tasks. No new unresolved
step-2 regressions found. Changes are uncommitted.

## 2026-10-29: independent step 1 double-check — Codex (GPT-6)

Reviewed the uncommitted working tree on `763b169` against the original import
`fd32ac5`, using a separate manifest/content comparison as well as the check
script. **Step 1 is complete; no new cleanup findings.**

- Derived expected removals from the authorized directory/file list and compared
  them with the actual filesystem (including hidden files). Exactly 42 removed:
  12 `etc/` defaults, five systemd units/presets, one polkit action, ten SDDM
  files, eight unused lockscreen files, four hidden-widget files and two helper
  scripts. No unexpected missing or added payload files.
- Checked all 369 retained payload files against their original Git blob hashes
  and permissions. Exactly one file differs: the panel layout. Its only logical
  change is removing `com.kde.plasma.nobara.runcommand`; all other code and
  widget ordering are preserved. Repository LICENSE is unchanged.
- Preserved byte-for-byte: 284 GTK/theme files, 12 Aurorae files, two Konsole
  files, 25 wallpapers, one Plasma Login wallpaper, three custom icons and
  20 Plasma-style files. Remaining global-theme, layout and Peek at Desktop
  files are present. No symlinks or executable payload files remain.
- Searched retained QML, JS, metadata and configuration for removed helper
  names, pkexec, papirus-folders and system-setting commands. No functional
  references remain. The only SDDM mention is an existing positioning comment
  in `contents/splash/Splash.qml:30`, not a dependency or behavior.
- `bash -n tools/check.sh` and `git diff --check`: pass.
- Reran `tools/check.sh`: scope validation, JSON, SVGZ and Plasma discovery
  pass. Exactly the same two GTK dark-import failures remain (finding 6).
  Retained QML warning counts are unchanged (splash 1; Peek at Desktop 13/0/3).

Limits: no live desktop/login tests or installation. This verifies the cleanup;
remaining compatibility fixes and optional Aurorae repair are later steps.
No payload changes were needed during this review. Audit/changelog updates and
all earlier cleanup changes remain uncommitted.

## 2026-10-29: step 1 cleanup verification — Codex (GPT-6)

Audited working tree based on `763b169`, after the user authorized step 1.
This review supersedes the earlier unmodified-payload status.

Changes and resolved findings:

- Removed all 12 `etc/` defaults, including forced GTK preferences and the
  screen-lock disable settings (finding 7).
- Removed the Nobara polkit action (finding 1).
- Removed the hidden run-command plasmoid (4 files), its panel-layout entry,
  and the apply/clean scripts (findings 2 and 3).
- Removed the three systemd user units and two presets (finding 11).
- Removed the SDDM theme (10 files, including its hidden face image), as requested.
- Removed the unused global-theme lockscreen folder (8 files, finding 9).
- Total: 42 files removed. No other appearance files were deleted. The Aurorae
  artwork remains for later optional repair (finding 10).
- Updated SOURCE.txt and checks for the reduced payload. Original files remain
  available in import commit `fd32ac5` and `../nobara/kde-nobara`.

Validation:

- `bash -n tools/check.sh` and `git diff --check`: pass.
- New scope checks: retained components present, excluded directories absent,
  and no references to removed helpers, pkexec or papirus-folders in retained
  payload files.
- JSON metadata, compressed SVG and Plasma package listing: pass.
- `tools/check.sh`: **2 known failures**, both unchanged GTK 3/4 dark-variant
  imports from finding 6. No new check failures.
- Remaining QML warnings: splash 1 (stock 1); Peek at Desktop main 13,
  Controller 0, MinimizeAllController 3, unchanged from the baseline. Counts are
  informational and do not establish runtime correctness.
- Retained GTK, Konsole, icons, wallpapers, Plasma Login, Aurorae and other
  appearance files are unchanged; only the panel layout loses a widget entry.

Limits: no live theme/login/panel testing, no package installation, no user or
system configuration changes. This step does not fix the invalid widget-style
name, other Plasma compatibility issues, or GTK imports. No new issues found
in the cleanup itself. Work remains uncommitted.

## 2026-10-29: scope and Plasma Login review — Codex (GPT-6)

Reviewed local commit `763b169` (unchanged payload) and KDE's
`plasma-login-manager` source at tag `v6.8.2`. This is a source/documentation
review; no greeter was launched and no installed settings were changed.

The user narrowed scope to Plasma theme, wallpapers, icons and Plasma Login,
then explicitly confirmed retaining the Nobara Konsole profile/color scheme
and GTK 2/3/4 themes on 2026-10-29. SDDM, distro defaults, helper scripts, custom
polkit actions and systemd integration are excluded. Findings about excluded
components remain here as historical evidence; future fixes should remove those
components rather than repair them. GTK finding 6 is still relevant and needs
review; the GTK assets themselves are retained while forced global GTK settings
are excluded. Implementation has not started.

Plasma Login findings:

- Local import: `usr/share/plasmalogin/wallpapers/nobara/nobara-winds1.webp` is
  the sole Plasma Login file. It is wallpaper artwork, not a greeter theme.
- KDE `src/frontend/greeter/main.cpp`: each greeter window loads
  `qrc:/qt/qml/org/kde/plasma/login/Main.qml`, a built-in interface. There is no
  SDDM theme path to reuse in the reviewed code.
- KDE `src/frontend/kcm/ui/main.qml`: "Apply Plasma Settings" explicitly
  supports color scheme, cursor and Plasma theme (among other settings), and
  says that theme/font files must be installed globally.
- KDE `src/frontend/kcm/kcm.cpp`, `synchronizeSettings()`: submits `kdeglobals`,
  `plasmarc` and other desktop configs to the standard authenticated helper;
  `auth/plasmaloginauthhelper.cpp` writes them under the greeter account.
- KDE `src/frontend/settings/plasmaloginsettingsbase.kcfg` and the Appearance
  page expose the wallpaper plugin and wallpaper configuration.
- Installed package: `plasma-login-manager 6.8.2-1`. Its documented optional
  `/usr/lib/plasmalogin/defaults.conf` does not exist here. Do not assume it
  exists, overwrite it, or ship a distro configuration to apply theme assets.

Conclusion: support Nobara login appearance with globally installed resources,
KDE's existing appearance-sync action, and wallpaper selection. A separate
replaceable SDDM-style greeter theme is not supplied by Nobara or the reviewed
Plasma Login configuration API. Explain this in the README.

Sources:

- [KDE Plasma Login 6.8.2 README](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/README.md)
- [KCM appearance sync and global-install requirement](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/src/frontend/kcm/ui/main.qml)
- [Greeter loading](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/src/frontend/greeter/main.cpp)

Validation: reviewed installed file inventory, upstream source and local git
status. `git diff --check` passes. `tools/check.sh` reproduces the two expected
GTK dark-import failures; JSON, SVGZ and package discovery pass, with QML warning
counts matching the original baseline. No theme or greeter runtime testing.

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

User decision (D6, 2026-10-29): keep the files and work on them later as an
optional decoration. The layout problem remains open; fix and validate the
package layout before shipping it. Breeze remains the default. Metadata says
it is by Vince Liuice (WhiteSur/Orchis author), GPL v3.

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
