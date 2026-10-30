# nobara-6-8-3 changelog

Newest first. One entry per agent session: date, agent, what changed, check
results, anything left half done, what's next. See `AGENTS.md` for the rules.

## 2026-10-29, Codex (GPT-6): v0.1.0 GitHub release

- User authorized release publication. Prepared tag/release v0.1.0 with the
  checksummed source archive, Arch package 0.1.0-1, PKGBUILD, .SRCINFO and SHA256SUMS.
- Changed the recipe from local-only source to the version-pinned GitHub release
  asset URL, keeping an actual SHA-256. Updated README/build instructions and
  shared notes for release downloads versus development snapshots.
- Full tools/check.sh passes; regenerated source and rebuilt/checked the package
  for the release documentation. All 1,705 icon links and installation exclusions
  remain intact. No theme artwork or palette changes; prior runtime checks apply.
- Preserved prior test limits and documented required Papirus/Breeze components,
  source-only Aurorae, and Plasma Login-only appearance support in release notes.
- Release preparation committed and pushed; generated artifacts remain outside
  Git history. No AUR upload, system installation or theme activation. In progress:
  nobody. Later releases must use a new version rather than replacing assets.

## 2026-10-29, Codex (GPT-6): GitHub repository setup

- User authorized creating/setup of the GitHub repository, using Vapor as the
  reference. Created public orlfman/nobara-plasma-6.8 and connected origin.
- Reworked README with Vapor-style contents table, fixes, clone/build/install,
  appearance/login selection, compatibility and license/credits sections.
  Added CONTRIBUTING.md and a GitHub theme bug-report form. Set the repository
  description/topics and retained the standard Issues/Projects/Wiki features.
- Updated project/packaging URLs and shared handoff notes. Included contribution
  guidance in generated source snapshots; retained local-only source packaging.
- Credential/private-key pattern scan and oversized-file scan found no matches.
  Full structural/GTK/QML/icon checks pass. Regenerated the source/checksum and
  local package for the updated documentation; no runtime artwork/palette edits.
- Committed stages 1–5 and repository setup together as the initial adaptation,
  preserving the upstream import and original agent-doc history. Generated
  archives remain ignored/local. No tagged release, AUR upload, system install
  or live settings changes. In progress: nobody.

## 2026-10-29, Codex (GPT-6): stage 5 local Arch package

- Prepared local plasma6-themes-nobara-fixed 0.1.0-1 with PKGBUILD, .SRCINFO,
  explicit runtime manifest and checksummed source snapshot of the current
  working tree, including uncommitted work. Source archives preserve Aurorae
  and authored templates; the binary package excludes those unrepaired/source
  components. No appearance files, palettes or GTK/Konsole colors were changed.
- Required Papirus and Breeze GTK plus the Plasma/Breeze/cursor components;
  Konsole and Plasma Login are optional consumers. Verified the separate Breeze
  cursors dependency by installed file ownership. No automatic settings actions.
- Added tools/prepare-package.py and tools/check-package.py, and made the source
  install manifest part of tools/check.sh and makepkg checks. Actual package
  verification covers exact bytes, links, scope, root ownership, modes and deps.
- Built successfully: 1,950 files/links, including 1,705 intact icon links.
  namcap: zero errors, ten manually reviewed data/transitive-dependency warnings.
  No current install-file collisions. Extracted-package KDE theme/wallpaper/icon
  probes, full checks, four builder regressions and isolated runtime checks pass.
- Added PACKAGING.md with build, install/removal, warning explanations and later
  publication requirements; updated README, login instructions, agent guide,
  audit and plan. The recipe is local-only until a public release is authorized.
- All prior work and this stage remain uncommitted. No installation, theme or
  login settings changes, commit, GitHub/AUR creation or push. In progress:
  nobody. Live visual/login testing and optional Aurorae repair remain deferred.

## 2026-10-29, Codex (GPT-6): runtime/performance compatibility audit

- Measured a splash performance defect: an infinite animation targeted an Image
  with no source. Removed that invisible animation while preserving the layout
  anchor, wallpaper, intro and progress transitions; qualified root.stage.
- Isolated idle measurement went from 567 redraws / 40.801 ms CPU over about
  three seconds to 0 redraws / 0.038 ms CPU. Settled captures are pixel-identical.
  These are offscreen software results, not live GPU/session measurements.
- Added tools/check-runtime.sh, a compiled splash-idle regression and mocked
  task-manager QtTest fixtures for the actual Minimize All controller. Four
  behavioral cases plus init/cleanup pass; no real windows are touched.
- Benchmarked icon lookup/rendering against Papirus-Dark over five runs each:
  similar cached request cost and peak memory, small initial lookup difference.
  Compared controller code against KDE v6.8.2; no further blocker found.
- Full structural/GTK/QML checks, four icon-builder tests, KDE package/theme/
  image/icon probes and shell/diff checks pass. SVG filter/reference scan clean.
- Added PERFORMANCE.md with methods, numbers and limitations; updated README,
  AGENTS, PLAN and AUDIT. All earlier work and these changes are uncommitted.
  No installation, actual desktop/login settings changes, commit or push.
- In progress: nobody. Live KWin/session/login/GPU testing and optional Aurorae
  repair remain deferred; await the user's next task.

## 2026-10-29, Codex (GPT-6): step 4 audit and GTK 2 removal

- Audited steps 1–3 together. Found and fixed icon-builder data loss on a failed
  rebuild: validate dependency targets first, roll back failed publication,
  preserve a recovery backup if restoration fails. Added four passing failure/
  recovery regression tests; the original disposable-copy reproduction now passes.
- Added an enforced syntax gate for retained QML/JS; warning totals alone did not
  catch syntax failures. All retained files pass; malformed fixture is rejected.
- User instructed dropping GTK 2 during the audit. Removed gtk-2.0 (12 files)
  and 99 GTK2-only PNG assets, preserving the 167 assets used/retained for GTK 3/4.
  Updated scope notes, README and checks. No GTK 2 engine dependency remains.
- Expanded CSS reference checks found root window_decorations.css pointed at
  24 SVGs never present upstream. Confirmed it is unused by retained themes and
  KDE's loader, then removed it; main GTK CSS still supplies existing titlebar
  glyphs. Corrected the earlier audit's inaccurate claim that its targets existed.
- Full checks and four regression tests pass. Final image validation: 176 raster
  images decode, 51 SVG/XML files parse. Current KDE icon/package probes pass;
  icon inheritance/aliases, metadata, wallpaper discovery and credits reviewed.
- Preserved original palette choices, Konsole, Aurorae and login resources.
  Recorded live-testing limits and optional black-color choice. Updated all
  shared docs; see AUDIT.md for evidence, sources and fixed findings.
- All changes from steps 1–4 remain uncommitted. No package installation, active
  desktop/login changes, commit or push. In progress: nobody. Await next task;
  optional Aurorae repair and actual visual tests remain deferred.

## 2026-10-29, Codex (GPT-6): step 3 icons and Plasma Login support

- Added a separate generated Nobara icon theme inheriting Papirus-Dark. It uses
  installed violet artwork, preserves small native icons, follows folder aliases
  across contexts/scales, and links the three original Nobara branding icons.
  Global defaults now select this overlay. Papirus remains a required dependency;
  no full icon set or folder-recoloring runtime helper is bundled.
- Added tools/build-icons.py (--build / read-only --check); connected checks to
  check.sh, and taught check-theme.py to verify the selected icon theme.
- Added README.md, ICONS.md and PLASMA-LOGIN.md: contents, dependencies, icon
  generation and desktop/login activation with explicit testing limits. Updated
  AGENTS.md, PLAN.md and AUDIT.md for the implementation and handoff.
- Checks pass: all 1,705 links resolve; KDE folder/alias lookups at normal/high-DPI
  sizes, branding rendering and login-action fallback pass in system-search and
  per-user test layouts. Stock mock login greeter loads offscreen with Nobara
  appearance and no QML/resource errors. No real authentication or sync action
  was invoked; actual login visuals still need a check after installation.
- Original Papirus links, Nobara branding, colors, GTK, Konsole, wallpapers and
  optional Aurorae artwork remain unchanged. No installed/user settings changed.
- All work from steps 1–3 remains uncommitted. No install, commit or push was
  requested. In progress: nobody. Next: full re-audit/documentation consolidation;
  optional Aurorae repair remains deferred.

## 2026-10-29, Codex (GPT-6): step 2 compatibility fixes

- Global defaults: explicit Breeze widget style; removed stale window/desktop
  switcher settings and ignored splash/breezerc entries. Added the Nobara
  wallpaper package default without forcing a user's existing wallpaper.
- Plasma style: preserved contrast/adaptive transparency settings in `plasmarc`,
  corrected fallback wallpaper suffix/dimensions, and corrected its JSON ID to
  `Nobara`. Removed duplicate Plasma-style/global-theme legacy metadata; full
  original metadata (including credits/licenses) is in UPSTREAM-NOTICES.md.
- Wallpaper: moved the existing winds WebP unchanged into
  `wallpapers/Nobara/contents/images/3840x2160.webp` and added metadata. Removed
  the folder setup script's hardcoded path. Splash and Plasma Login images stay
  unchanged, as do the other 24 wallpaper images.
- Application colors: corrected internal scheme name MateriaDark -> Nobara;
  every palette value remains unchanged. Header fallback remains valid.
- GTK review: main stylesheets are light; dark variants explicitly load
  Breeze-Dark. Preserved both appearances, fixing the dark imports to system
  file URLs so per-user installs work. `breeze-gtk` is required for future
  packaging/documentation, in addition to the user-required papirus-icon-theme.
- Removed confirmed-unused busywidget.svgz, fedora-logo-sprite_classic.svg,
  panel-background_backup.svgz, and the empty upstream `.codex` file. Preserved
  authored templates, GTK artwork, Konsole, icons, Peek at Desktop and Aurorae.
- Added tools/check-theme.py and connected it to check.sh for compatibility
  settings and file references. Updated shared docs and handoff status.
- Validation: all project checks pass, including all four GTK CSS variants.
  KDE package/config/theme/image probe passes in isolated system-search and
  copied per-user layouts. Effect/color comparisons and image hashes match the
  import; QML warning counts unchanged. See AUDIT.md for evidence and limits.
- All changes, including earlier cleanup/docs, remain uncommitted. Nothing was
  installed or applied to the user's session; no push. In progress: nobody.
- Next: icon inheritance/violet folders and Plasma Login appearance validation.
  Aurorae repair remains optional, for later work.

## 2026-10-29, Codex (GPT-6): double-check step 1

- Independently compared the current payload against import `fd32ac5` while HEAD
  remains `763b169`. Exactly the authorized 42 files are gone. All 369 retained
  files are present, with no extras or changed modes; content matches upstream
  except for the intended hidden-widget entry removal in the panel layout.
- Verified GTK, Aurorae, Konsole, wallpapers, Plasma Login resources, custom
  icons, Plasma style and LICENSE are preserved. Checked hidden files and
  symlinks as well. No functional references to the removed integration remain.
- Reran the checks: scope/metadata/SVGZ/discovery pass; exactly two existing GTK
  dark-import failures remain. QML counts are unchanged. Syntax/diff checks pass.
- Recorded detailed evidence and testing limits in AUDIT.md. No new findings or
  further payload changes. Step 1 is complete; next is compatibility fixes.
- All cleanup and documentation changes remain uncommitted. No installation,
  user/system setting changes, commits or pushes. In progress: nobody.

## 2026-10-29, Codex (GPT-6): step 1 scope cleanup

- User authorized step 1. Removed 42 files: the 12 distro defaults under `etc/`,
  Nobara's polkit action, the four-file hidden run-command widget, the two
  apply/clean scripts, five systemd units/presets, 10 SDDM files (including
  `faces/.face.icon`), and eight unused global-theme lockscreen files.
- Removed the hidden command widget entry from the Nobara panel layout. The
  visible panel widgets and Peek at Desktop remain.
- Preserved GTK 2/3/4, Konsole, wallpaper collection, all three custom icons,
  Plasma Login wallpaper, splash and Plasma style artwork, plus the optional
  Aurorae decoration for later repair. No colors or appearance were changed.
- Updated SOURCE.txt to identify the modified working copy. Updated
  tools/check.sh to check retained assets, excluded integration and removed
  helper references, and stop linting the removed SDDM/lockscreen files.
- Updated AGENTS.md, PLAN.md and AUDIT.md for cleanup and handoff.
- Validation: shell syntax and diff checks pass; scope checks, JSON, SVGZ and
  Plasma package listing pass. The complete check script still reports exactly
  the two known GTK dark-import failures (AUDIT 6). Remaining QML counts match
  the previous baseline. No live session/login tests or installation.
- Uncommitted work: all changes in this entry and the earlier scope notes.
  No commits or pushes were requested. In progress: nobody.
- Next: remaining Plasma 6.8.2 compatibility fixes, then GTK import review and
  icon/login appearance work. Aurorae repair is deferred.

## 2026-10-29, Codex (GPT-6): visual-only scope and Plasma Login review

- User clarified scope: KDE Plasma theme, wallpapers, icons, and Plasma Login
  appearance, and subsequently confirmed retaining the Nobara Konsole and
  GTK 2/3/4 themes. Exclude SDDM and distro integration. Recorded D1–D8 decisions
  and revised work sequence in PLAN.md; AGENTS.md now reflects this scope.
- Inspected Plasma Login source at `v6.8.2` and the installed 6.8.2-1 package.
  Nobara provides only a login wallpaper. Supported login appearance comes from
  globally installed theme assets, "Apply Plasma Settings", and the wallpaper
  selector. Recorded evidence and limits in AUDIT.md.
- Icons: proposed assessing a Papirus-Dark-inheriting Nobara overlay for violet
  folders and branding, with no automatic edits to the system Papirus theme.
- User confirmed `papirus-icon-theme` as a required runtime dependency of the
  future theme package (`depends`, not `optdepends`). Recorded in AGENTS.md and
  PLAN.md; reuse installed Papirus rather than bundling the full icon set.
- User confirmed retaining `usr/share/konsole/Nobara.profile` and
  `Nobara.colorscheme`; corrected the scope notes in AGENTS.md, PLAN.md and
  AUDIT.md. No additional terminal theme was requested.
- User confirmed retaining Nobara GTK themes as well (GTK 2/3/4 and assets).
  Corrected all scope notes; GTK dark-variant import finding 6 remains open.
  Forced GTK settings under `etc/` are still excluded as distro defaults.
- User confirmed retaining Aurorae artwork for later repair as an optional
  appearance. Updated D6 and the cleanup exclusions; Breeze stays the default.
- No Nobara payload changes; no installation, settings changes, commits or
  pushes. The documentation changes are intentionally uncommitted.
- Validation: `git diff --check` passes. `tools/check.sh` reproduces the same
  two expected GTK dark-import failures from the original audit. JSON, SVGZ and
  package discovery pass; QML warning counts match the recorded baseline.
- Next: implement the scoped removals and Plasma 6.8.2 fixes when requested.

## 2026-10-29, Claude Code (Claude Opus 5.5): import, agent docs, first audit

- Copied Nobara's `kde-nobara/` (6.7.5, nobara-core-packages `4794fa0c`,
  2026-10-18) into this folder unmodified, with `SOURCE.txt`. Nobara hasn't
  changed it since the first download earlier the same day.
- Set up the repo for Claude Code and Codex: `AGENTS.md` (shared rules,
  turn-taking, checks), `CLAUDE.md` (imports AGENTS.md), `PLAN.md`, `AUDIT.md`,
  this file, `tools/check.sh` and `tools/check-gtk-css.py`, `.gitignore`.
- git: first commit = the unmodified import, second = docs and tools. Local only,
  no remote. Nobara's files unchanged.
- Audited against Plasma 6.8.2 (source read at tag v6.8.2 for plasma-workspace,
  libplasma, kwin, kscreenlocker): 16 findings, see AUDIT.md. Most serious: a
  polkit rule giving any user passwordless root for `papirus-folders`, and a
  hidden panel widget that runs the theme script (which never finishes) at
  every Plasma start.
- The user confirmed on a real Nobara 44 boot that it uses the Breeze widget
  style (matches AUDIT finding 4).
- `tools/check.sh` on the unmodified import: 2 checks failed, both expected
  (the `gtk-dark.css` imports of Breeze-Dark, AUDIT finding 6). JSON, svgz and
  Plasma listing pass; qmllint counts match stock for splash and SDDM.
- Next: the user answers PLAN.md decisions D1–D8; meanwhile step 2 (fixes that
  need no decision) can start when the user says so.
