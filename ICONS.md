# Nobara icon theme

`usr/share/icons/Nobara` is an inheriting theme, named **Nobara**, with
`Inherits=Papirus-Dark`. The full icon set comes from required
`papirus-icon-theme`; the overlay adds violet folders and three Nobara icons.

## How it works

The overlay links generic folder/home names to Papirus's existing violet SVGs.
It follows the operation used by upstream `papirus-folders` (real violet
folder/user files at sizes 22, 24, 32, 48, 64) but builds separate files rather
than editing Papirus's symlinks. It follows aliases from all indexed contexts,
including `folder-downloads`, `inode-directory`, and matching app/category/MIME
aliases, so inheritance cannot accidentally reintroduce blue folders.

Directory sizes/types/scales are copied from Papirus-Dark's index. High-DPI and
large scalable variants are covered; native 16px monochrome forms are preserved.
The existing Nobara hicolor artwork is referenced by relative links from the
overlay, so it wins theme lookup while its original files remain intact.

Papirus artwork links use absolute `/usr/share/icons/Papirus...` paths. This is
intentional: the required base package is installed system-wide. It also lets a
per-user Nobara overlay use that same base. Neither generated links nor build
scripts modify the installed Papirus themes.

## Regenerating and checking

From the project directory:

```sh
python3 -I tools/build-icons.py --build
python3 -I tools/build-icons.py --check
```

The builder writes only the project's generated `usr/share/icons/Nobara` folder.
It checks dependency targets before replacing existing output, restores the
old theme if publication fails, and retains a recoverable backup path if even
restoration fails. Run `python3 -I tools/test-icon-builder.py` for the four
disposable-fixture regression tests.
Do not keep hand edits in that generated folder. Source branding lives in
`usr/share/icons/hicolor`; the generator is `tools/build-icons.py`.

Current verification uses Papirus `20260801-1`. If an update changes the artwork
paths or aliases, the check detects drift or missing targets; regenerate and
validate before publishing a new theme package. No post-install recoloring hook
or `papirus-folders` dependency is needed.

KDE's icon loader was checked in isolated system-search and per-user layouts.
See AUDIT.md for tested sizes/scales and testing limits.

Reference: [Papirus folder-color helper](https://github.com/PapirusDevelopmentTeam/papirus-folders/blob/master/papirus-folders)
and [Papirus icon theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme).
