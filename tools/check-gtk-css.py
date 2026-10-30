#!/usr/bin/env python3
"""Parse a GTK CSS file with the system GTK and print its parse errors.

Usage: python3 -I tools/check-gtk-css.py 3.0|4.0 FILE.css
Prints "N errors" and the first errors. Exit status 0 only with 0 errors.
"""
import sys

import gi

if len(sys.argv) != 3 or sys.argv[1] not in ("3.0", "4.0"):
    sys.exit(__doc__)

version, path = sys.argv[1], sys.argv[2]
gi.require_version("Gtk", version)
from gi.repository import Gtk  # noqa: E402

errors = []


def on_error(_provider, section, error):
    if version == "3.0":
        line = section.get_start_line()
    else:
        line = section.get_start_location().lines
    errors.append(f"{line + 1}: {error.message}")


provider = Gtk.CssProvider()
provider.connect("parsing-error", on_error)
try:
    provider.load_from_path(path)
except Exception as exc:  # GTK 3 raises on fatal errors such as a failed @import
    errors.append(f"load: {exc}")

print(f"{len(errors)} errors")
for message in errors[:10]:
    print(message)
sys.exit(0 if not errors else 1)
