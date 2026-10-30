#!/usr/bin/env bash
# Isolated runtime regressions; writes/compiles only in a disposable /tmp folder.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work="$(mktemp -d /tmp/nobara-runtime-test.XXXXXX)"
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/config" "$work/data" "$work/cache" "$work/state" "$work/runtime"
chmod 700 "$work/runtime"
export QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software
export XDG_CONFIG_HOME="$work/config" XDG_DATA_HOME="$work/data"
export XDG_CACHE_HOME="$work/cache" XDG_STATE_HOME="$work/state" XDG_RUNTIME_DIR="$work/runtime"
export DBUS_SESSION_BUS_ADDRESS=unix:path=/nonexistent
/usr/lib/qt6/bin/qmltestrunner -input "$root/tools/qml-tests" -import "$root/tools/qml-tests/mocks" -o -,txt
g++ -std=c++17 -fPIC "$root/tools/check-splash-idle.cpp" -o "$work/splash-idle" $(pkg-config --cflags --libs Qt6Quick)
"$work/splash-idle" "$root/usr/share/plasma/look-and-feel/org.nobaraproject.desktop/contents/splash/Splash.qml"
