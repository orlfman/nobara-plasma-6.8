# Contributing

Report appearance or compatibility problems through GitHub Issues. Include your
distribution, Plasma/Qt versions, installed theme components, steps to reproduce,
and screenshots when useful. For icons, include the Papirus package version;
for GTK, identify GTK 3 or GTK 4 and the application. Remove personal information
from logs and screenshots before posting them.

This project preserves Nobara's appearance for Plasma 6.8.2. Keep proposed fixes
focused and explain the affected behavior. Visual redesigns, new components and
Aurorae repair should be discussed before implementation. Breeze stays the
default, Papirus is required, GTK 2 and SDDM are excluded, and installation must
not change user settings, authentication or distribution policy.

Read AGENTS.md and PLAN.md for shared project rules. Run tools/check.sh after
changes and the relevant isolated regressions for runtime or builder changes.
Do not test by executing removed Nobara setup scripts or altering the live
session. Document verification and remaining limits in AUDIT.md and changes in
CHANGELOG.md. Build output and generated source archives belong outside commits.
See PACKAGING.md for source regeneration and actual package verification.
