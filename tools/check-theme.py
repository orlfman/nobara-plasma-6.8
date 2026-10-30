#!/usr/bin/env python3
"""Read-only checks for Plasma defaults, migrated settings and local asset links."""
import configparser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

root = Path(__file__).resolve().parent.parent
share = root / "usr/share"
lnf = share / "plasma/look-and-feel/org.nobaraproject.desktop"
style = share / "plasma/desktoptheme/Nobara"
failures = []


def check(ok, message):
    if not ok:
        failures.append(message)
        print("FAIL:", message)


def config(path):
    result = configparser.ConfigParser(interpolation=None)
    result.optionxform = str
    with path.open() as handle:
        result.read_file(handle)
    return result


def value(conf, group, key):
    return conf.get(group, key, fallback="")


try:
    defaults = config(lnf / "contents/defaults")
    check(value(defaults, "kdeglobals][KDE", "widgetStyle") == "Breeze", "widget style must be Breeze")
    check(value(defaults, "kwinrc][org.kde.kdecoration2", "library") == "org.kde.breeze", "default window decoration must remain Breeze")
    for group in ("kwinrc][WindowSwitcher", "kwinrc][DesktopSwitcher", "KSplash", "breezerc][Common"):
        check(not defaults.has_section(group), f"obsolete defaults group: {group}")
    check(value(defaults, "kdeglobals][Icons", "Theme") == "Nobara", "global theme must select the Nobara icon overlay")
    check(value(defaults, "Wallpaper", "Image") == "Nobara", "default wallpaper package must be Nobara")
    check(not (lnf / "contents/plasmoidsetupscripts/org.kde.plasma.folder.js").exists(), "hardcoded wallpaper setup script remains")

    rc = config(style / "plasmarc")
    for key, expected in (("enabled", "true"), ("contrast", "1.0"), ("intensity", "1.0"), ("saturation", "1.0")):
        check(value(rc, "ContrastEffect", key) == expected, f"ContrastEffect/{key} changed")
    check(value(rc, "AdaptiveTransparency", "enabled") == "true", "adaptive transparency must remain enabled")
    check(value(rc, "Wallpaper", "defaultWallpaperTheme") == "Nobara", "Plasma style wallpaper package is wrong")
    check(value(rc, "Wallpaper", "defaultFileSuffix") == ".webp", "wallpaper suffix does not match image")
    check(value(rc, "Wallpaper", "defaultWidth") == "3840" and value(rc, "Wallpaper", "defaultHeight") == "2160", "wallpaper dimensions are wrong")

    for folder, expected in ((style, "Nobara"), (lnf, "org.nobaraproject.desktop"), (share / "wallpapers/Nobara", "Nobara")):
        metadata = json.loads((folder / "metadata.json").read_text())
        check(metadata["KPlugin"]["Id"] == expected, f"incorrect plugin id: {folder.relative_to(root)}")
    check((share / "wallpapers/Nobara/contents/images/3840x2160.webp").is_file(), "packaged default wallpaper is missing")
    check(value(config(share / "color-schemes/Nobara.colors"), "General", "ColorScheme") == "Nobara", "leftover internal color scheme name")
    check((root / "UPSTREAM-NOTICES.md").is_file(), "preserved upstream metadata notices are missing")
    for path in (style / "metadata.desktop", lnf / "metadata.desktop", style / "widgets/panel-background_backup.svgz", lnf / "contents/splash/images/busywidget.svgz", lnf / "contents/splash/images/fedora-logo-sprite_classic.svg", root / ".codex"):
        check(not path.exists(), f"obsolete file remains: {path.relative_to(root)}")

    for version in ("3.0", "4.0"):
        path = share / f"themes/Nobara/gtk-{version}/gtk-dark.css"
        expected = f'@import url("file:///usr/share/themes/Breeze-Dark/gtk-{version}/gtk.css");'
        check(path.read_text().strip() == expected, f"dark GTK {version} must retain its Breeze Dark provider")

    # CSS parsing does not necessarily detect missing image assets. Check URLs too.
    theme_css = sorted((share / "themes/Nobara").rglob("*.css"))
    for css in theme_css:
        for url in re.findall(r"url\(\s*[\"']?([^\"')\s]+)", css.read_text()):
            parsed = urlparse(url)
            if parsed.scheme == "file":
                target = Path(unquote(parsed.path))
            elif not parsed.scheme:
                target = css.parent / unquote(url)
            else:
                continue
            check(target.is_file(), f"missing CSS asset/import: {css.relative_to(root)} -> {url}")

    for qml in (lnf / "contents/splash").glob("*.qml"):
        for relative in re.findall(r'^\s*source:\s*"(images/[^"\n]+)"', qml.read_text(), re.M):
            check((qml.parent / relative).is_file(), f"missing splash image: {relative}")
except (OSError, KeyError, ValueError, configparser.Error) as exc:
    failures.append(str(exc))
    print("FAIL:", exc)

if failures:
    sys.exit(1)
print("Plasma defaults, migrated settings, wallpaper and CSS references: PASS")
