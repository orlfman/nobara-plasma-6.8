# nobara-6-8-3 changelog

Newest first. One entry per agent session: date, agent, what changed, check
results, anything left half done, what's next. See `AGENTS.md` for the rules.

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
