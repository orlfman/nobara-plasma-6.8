# Runtime, performance and compatibility audit

Reviewed 2026-10-29 on Plasma Workspace/Desktop/libplasma/Breeze **6.8.2**,
Plasma Login Manager **6.8.2**, Qt **6.12.0**, Papirus **20260801-1**.
Tests used isolated configuration/cache/data/state paths. The running desktop
and login manager were not reconfigured.

## Fixed: invisible splash animation

Nobara's splash animated an Image whose source was commented out. Its infinite
scale loop still caused redraws even though the image was empty. Removed only
the unused animation; the positioning item, wallpaper, progress bar, intro and
progress transitions remain. Also qualified the progress binding as root.stage.

A 1280x800 offscreen software-rendered view was allowed to finish its intro,
then observed for about three seconds:

| Settled splash | Frame swaps | CPU time during observation |
| --- | ---: | ---: |
| Before | 567 | 40.80 ms |
| After | 0 | 0.038 ms |

These are bounded software-test measurements, not live GPU/compositor frame
rates or a claim about whole-system startup. Settled captures at stage 4 were
pixel-identical before and after the change.

`tools/check-runtime.sh` checks that the splash settles (at most two incidental
frames in the observation window), alongside controller behavior tests.

## Icon overhead

Five runs per theme, alternating order, with fresh per-process settings/caches.
Filesystem caches were not flushed. KIconLoader requested eight common folder,
application and action icons at four sizes, followed by 20,000 cached 32px
requests. Times exclude QGuiApplication initialization and are medians:

| Theme | Initial 32 requests | 20,000 cached requests | Peak process RSS |
| --- | ---: | ---: | ---: |
| Nobara | 18.84 ms | 11.09 ms | 37,712 KiB |
| Papirus-Dark | 18.31 ms | 10.95 ms | 37,728 KiB |

This workload shows a small initial lookup difference and similar cached cost
and memory footprint. It does not establish a meaningful application-startup
penalty, nor cover every icon or real application. No need to remove the violet
folder overlay on performance grounds was found.

## Runtime compatibility checks

- KDE's package/config/image/theme APIs load the Nobara theme and wallpaper.
- KDE icon lookup tests cover 96 folder size/scale/alias combinations, branding
  rasterization and inherited login/action icons.
- The actual MinimizeAllController is tested with a mock org.kde.taskmanager
  module: activity/desktop filtering and restoration, manually restored/closed
  windows, focus changes, empty models and desktop state changes. No real
  window-management methods are called. QtTest reports four test cases plus
  initialization/cleanup (six passes).
- Compared the controller with KDE's v6.8.2 source: its algorithm is the same;
  remaining differences are versioned imports and callback qualification.
- The retained panel drag-hover timer is one-shot and event-driven. No periodic
  polling, external-command widget or login helper was reintroduced.
- Runtime Plasma SVGs have no SVG filter/Gaussian-blur chains; internal gradient/
  clip references resolve. This is a complexity check, not a GPU benchmark.
- QML/JS syntax, metadata, GTK 3/4 parsing/assets, icon links and removed-component
  checks pass. Aurorae source is deliberately excluded from readiness claims.

Run:

```sh
tools/check.sh
python3 -I tools/test-icon-builder.py
tools/check-runtime.sh
```

The runtime check needs g++, pkg-config, Qt6Quick development headers/libraries,
and qmltestrunner. These are developer test requirements, not theme runtime
requirements. It compiles into a disposable /tmp directory and uses the software
offscreen platform. Its task-manager module is a test double guarded by an
assertion before any controller action.

## Remaining testing limits

No full Plasma session, live KWin window operations, actual login authentication,
monitor/accessibility behavior, live GTK application visuals or compositor/GPU
benchmark was exercised. The earlier mock-greeter smoke test checks resource/QML
loading only. Theme compatibility is supported by the checks above; deployment
still needs an authorized installation and visual testing. Optional Aurorae
repair remains separate. See AUDIT.md for the detailed history and evidence.
