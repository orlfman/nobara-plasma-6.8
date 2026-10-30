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

echo "== JSON metadata"
while IFS= read -r -d '' f; do
    python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' "$f" 2>/dev/null \
        || fail "invalid JSON: ${f#"$root"/}"
done < <(find "$root/usr" -name '*.json' -print0)

echo "== compressed SVG"
while IFS= read -r -d '' f; do
    gzip -t "$f" 2>/dev/null || fail "broken svgz: ${f#"$root"/}"
done < <(find "$root/usr" -name '*.svgz' -print0)

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

echo "== qmllint warnings (Nobara / stock 6.8.2)"
compare() {  # file stockfile
    local s="-"
    [ -f "$2" ] && s=$(lint_count "$2")
    printf '  %-60s %3s / %s\n' "${1#"$root"/}" "$(lint_count "$1")" "$s"
}
compare "$lnf/contents/splash/Splash.qml" \
    /usr/share/plasma/look-and-feel/org.kde.breeze.desktop/contents/splash/Splash.qml
for f in "$lnf"/contents/lockscreen/*.qml; do
    [ -e "$f" ] && compare "$f" "/usr/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/$(basename "$f")"
done
for f in "$share"/sddm/themes/nobara/*.qml; do
    [ -e "$f" ] && compare "$f" "/usr/share/sddm/themes/breeze/$(basename "$f")"
done
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
