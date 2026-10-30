# Plasma Login appearance

This project supports **Plasma Login Manager**, using its built-in login layout
with Nobara's colors, Plasma style, icons and wallpaper. It supplies appearance
assets, not replacement greeter QML or authentication/service configuration.

## Requirements

- Plasma Login Manager (reviewed against `6.8.2-1`).
- The reviewed Nobara appearance assets installed system-wide. A theme installed
  only in `~/.local/share` cannot be used by the separate login account.
- Required `papirus-icon-theme` for the Nobara icon overlay. Its parent theme and
  referenced violet artwork must remain available in `/usr/share/icons`.

Install the local package system-wide as described in [PACKAGING.md](PACKAGING.md),
then follow these activation steps. Package installation does not select a theme
or synchronize any settings to the login account.

## Activate through System Settings

1. Apply the Nobara global theme on the desktop. If choosing components
   separately, select Nobara colors, Plasma style and icons, with Breeze
   widgets/decorations and the Breeze cursor.
2. Open **Login Screen** for Plasma Login in System Settings.
3. Choose **Apply Plasma Settings…**, review the settings it will copy, and
   apply through KDE's normal authentication prompt. This action also copies
   desktop settings such as fonts, keyboard layouts and screen arrangement;
   review the full dialog rather than treating it as a theme-only operation.
4. Use the Login Screen wallpaper selector separately. Choose Nobara Winds or
   browse to the supplied login image:

   `/usr/share/plasmalogin/wallpapers/nobara/nobara-winds1.webp`

5. Apply the wallpaper change. Check the result at the next normal login.

The two actions are separate: “Apply Plasma Settings” does not itself select a
new login wallpaper. The settings module copies selected image resources into
the login account's wallpaper storage as needed.

If the desktop theme changes later, repeat the appearance-sync action when you
want that change on the login screen. Installing/updating this theme does not
silently overwrite the login account's chosen settings.

## Validation performed

- Confirmed the KCM copies `kdeglobals` and `plasmarc` through KDE's existing
  helper. The login startup code reconstructs global-theme defaults from the
  selected LookAndFeelPackage, including settings inherited from the theme.
- Tested the Nobara icon theme with KDE's loader, including login action icons
  inherited from Papirus-Dark.
- Checked Nobara Plasma resources and packaged wallpaper through KDE's package
  APIs, and checked the supplied login image is identical to the default image.
- Loaded the installed greeter offscreen with its `--test` mock authenticator
  and temporary appearance settings. This did not exercise real authentication
  or change the active display manager.

The actual login account's appearance, monitor layout, accessibility, and image
selection/synchronization still need a live check after an authorized install.
No real login settings have been changed during these tests.

Sources at KDE tag `v6.8.2`:

- [Appearance synchronization UI](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/src/frontend/kcm/ui/main.qml)
- [Appearance and wallpaper sync](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/src/frontend/kcm/kcm.cpp)
- [Login global-theme defaults](https://github.com/KDE/plasma-login-manager/blob/v6.8.2/src/frontend/startkde/startplasma.cpp)
