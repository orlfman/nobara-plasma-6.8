# nobara-6-8-3: plan

Status (2026-10-29): step 1 (import + audit) done. Nobara's files are still
unmodified; 16 findings are open in AUDIT.md (1 P1, 6 P2, 9 P3). Next: the user
answers the decisions below, then step 2.

In progress: nobody.

Agents: read `AGENTS.md` first (shared rules, turn-taking, checks).

## Goal

Nobara's KDE theme, fixed and checked for Plasma 6.8.2, the same way the SteamOS
Vapor theme was (`../steamos-vapor-6-8-3`): keep Nobara's look, fix what's
broken or outdated, drop what's distro plumbing, document every change.
Publishing (GitHub, AUR) only if and when the user asks.

## Decisions for the user

Agents: don't pick these yourself. Record the answer here with the date.

- **D1. polkit rule + Papirus folder color** (AUDIT 1). Drop the passwordless
  root rule? Then violet Papirus folders become a README step the user runs
  once (`sudo papirus-folders -C violet --theme Papirus-Dark`). Recommended: drop.
- **D2. Hidden run-command widget, apply/clean scripts, systemd units**
  (AUDIT 2, 3, 11). Recommended: remove all of it; the global theme plus a
  README covers what they did.
- **D3. GTK look** (AUDIT 6). Nobara forces dark, so GTK apps get Breeze-Dark
  through `gtk-dark.css`, not Nobara's own CSS. Keep that behavior (and drop the
  unused Nobara CSS?), or make the Nobara CSS the dark theme? Needs a look at a
  GTK 3 app on the user's Nobara 44 boot first. Also: keep GTK 2 (dropped in
  the Vapor project)?
- **D4. `etc/` distro defaults** (AUDIT 7). Recommended: leave out of any
  package (it turns off screen locking and sets system-wide fonts and defaults).
- **D5. Plasma style colors** (AUDIT 8). Breeze-blue highlights on black in
  panels vs purple in apps: intended, or switch the Plasma style to purple?
- **D6. Aurorae decoration** (AUDIT 10). Delete, or fix the folder layout and
  keep it as an optional "Nobara" window decoration?
- **D7. SDDM theme and plasmalogin wallpaper.** Keep in this project (the
  Nobara RPM ships them as separate `kde-nobara-sddm` / `kde-nobara-plasmalogin`
  packages)?
- **D8. Name and scope of a possible package**, e.g. a repo
  `nobara-plasma-6.8` and AUR `plasma6-themes-nobara-fixed`, plus Konsole and
  Alacritty colors like Vapor?

## Order of work

1. Done 2026-10-29: import kde-nobara 6.7.5 unmodified, set up docs and checks,
   full audit (AUDIT.md).
2. Uncontroversial fixes (no decision needed): `widgetStyle=Breeze` (AUDIT 4),
   remove the window/desktop switcher lines (5), remove dead `[KSplash]` and
   `[breezerc]` lines (13), delete the unused lock screen folder (9), color
   scheme leftovers (14), `plasmarc` for the Plasma style + drop legacy
   `.desktop` metadata (15), unused files (16), wallpaper package (12).
3. Apply the user's decisions D1–D7.
4. Re-audit everything, record in AUDIT.md.
5. Docs: README.md (what it is, what changed, install, license/credits), and
   CHANGES-style summary in CHANGELOG.md.
6. Only if the user asks: GitHub repo, PKGBUILD, AUR (D8).
