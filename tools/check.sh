#!/usr/bin/env bash
# Structural checks for the Nobara theme. Run from anywhere: tools/check.sh
# Read-only: writes no files. Plasma tools are only called with --list.
# Ends with "ALL CHECKS PASSED" or a list of failures (exit 1).
# qmllint warning counts are printed for comparison with stock Plasma, not judged.
set -u
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
share="$root/usr/share"
lnf="$share/plasma/look-and-feel/org.nobaraproject.desktop"
qmllint=/usr/lib/qt6/bin/qmllint
failures=()

fail() { failures+=("$1"); echo "FAIL: $1"; }
lint_count() { "$qmllint" -I /usr/lib/qt6/qml "$1" 2>&1 | grep -c 'Warning' || true; }

echo "== retained scope and excluded integration"
for item in etc usr/lib/systemd usr/share/polkit-1 usr/share/sddm \
    usr/share/themes/Nobara/gtk-2.0 \
    usr/share/plasma/plasmoids/com.kde.plasma.nobara.runcommand \
    usr/share/plasma/look-and-feel/org.nobaraproject.desktop/contents/lockscreen; do
    [ ! -e "$root/$item" ] || fail "excluded component remains: $item"
done
for item in color-schemes/Nobara.colors plasma/desktoptheme/Nobara \
    plasma/look-and-feel/org.nobaraproject.desktop/contents/splash/Splash.qml \
    plasma/layout-templates/org.kde.plasma.desktop.nobaraPanel \
    plasma/plasmoids/org.kde.plasma.nobara.showdesktop \
    wallpapers/Nobara/metadata.json wallpapers/Nobara/contents/images/3840x2160.webp \
    plasmalogin/wallpapers/nobara/nobara-winds1.webp \
    icons/hicolor/scalable/places/nobara-app-menu-icon.svg \
    icons/hicolor/scalable/actions/nobara-desktop-show-symbolic.svg \
    icons/hicolor/scalable/actions/nobara-desktop-hide-symbolic.svg \
    konsole/Nobara.profile konsole/Nobara.colorscheme \
    themes/Nobara/gtk-3.0 themes/Nobara/gtk-4.0 \
    themes/Nobara/assets aurorae/themes/Nobara aurorae/themes/metadata.desktop; do
    [ -e "$share/$item" ] || fail "retained resource missing: usr/share/$item"
done
# Excluded helper names must not survive in scripts, layouts, or configuration.
if matches=$(grep -rInE 'nobara-(apply|clean)-theme|com[.]kde[.]plasma[.]nobara[.]runcommand|pkexec|papirus-folders' "$share"); then
    echo "$matches"
    fail "reference to removed command-running integration"
else
    status=$?
    [ "$status" -eq 1 ] || fail "could not scan retained files for removed helpers"
fi

echo "== package install manifest"
python3 -I "$root/tools/check-package.py" --source || fail "package install manifest"

echo "== JSON metadata"
while IFS= read -r -d '' f; do
    python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' "$f" 2>/dev/null \
        || fail "invalid JSON: ${f#"$root"/}"
done < <(find "$root/usr" -name '*.json' -print0)

echo "== compressed SVG"
while IFS= read -r -d '' f; do
    gzip -t "$f" 2>/dev/null || fail "broken svgz: ${f#"$root"/}"
done < <(find "$root/usr" -name '*.svgz' -print0)

echo "== Plasma compatibility and asset references"
python3 -I "$root/tools/check-theme.py" || fail "theme defaults/config/assets"

echo "== Nobara icon theme and Papirus dependency"
python3 -I "$root/tools/build-icons.py" --check || fail "Nobara icon overlay/dependency"

echo "== GTK CSS (system parsers)"
for v in 3.0 4.0; do
    for f in "$share"/themes/Nobara/gtk-$v/*.css; do
        [ -e "$f" ] || continue
        out=$(GDK_BACKEND=wayland python3 -I "$root/tools/check-gtk-css.py" "$v" "$f" 2>/dev/null)
        echo "  ${f#"$share"/themes/}: ${out%%$'\n'*}"
        [ "${out%%$'\n'*}" = "0 errors" ] || fail "GTK $v CSS errors: ${f#"$root"/}"
    done
done

echo "== Plasma lists the packages (list only)"
export XDG_DATA_DIRS="$share:/usr/share"
plasma-apply-lookandfeel --list 2>/dev/null | grep -qx 'org.nobaraproject.desktop' \
    || fail "global theme not listed"
plasma-apply-colorscheme --list-schemes 2>/dev/null | grep -q ' Nobara' \
    || fail "color scheme not listed"
plasma-apply-desktoptheme --list-themes 2>/dev/null | grep -q ' Nobara' \
    || fail "Plasma style not listed"

echo "== QML and panel/setup JavaScript syntax"
while IFS= read -r -d '' f; do
    "$qmllint" --only-explicit-categories --syntax error --syntax.duplicate-ids error "$f" \
        || fail "QML/JS syntax error: ${f#"$root"/}"
done < <(find "$share/plasma" -type f \( -name '*.qml' -o -name '*.js' \) -print0)

echo "== qmllint warnings (Nobara / stock 6.8.2)"
compare() {  # file stockfile
    local s="-"
    [ -f "$2" ] && s=$(lint_count "$2")
    printf '  %-60s %3s / %s\n' "${1#"$root"/}" "$(lint_count "$1")" "$s"
}
compare "$lnf/contents/splash/Splash.qml" \
    /usr/share/plasma/look-and-feel/org.kde.breeze.desktop/contents/splash/Splash.qml
while IFS= read -r -d '' f; do
    compare "$f" ""
done < <(find "$share/plasma/plasmoids" -name '*.qml' -print0 2>/dev/null)

echo
if [ ${#failures[@]} -eq 0 ]; then
    echo "ALL CHECKS PASSED"
else
    echo "${#failures[@]} CHECK(S) FAILED"
    exit 1
fi
