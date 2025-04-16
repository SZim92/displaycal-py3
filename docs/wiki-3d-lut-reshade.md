# 3D LUTs for Direct3D and OpenGL Applications (using ReShade)

This guide explains how to use DisplayCAL-generated 3D LUTs with ReShade to implement color management in games and other 3D applications.

## Overview

Most games and 3D applications do not support color management, which can result in incorrect colors on calibrated displays. The [ReShade](https://reshade.me/) injector can be used with Direct3D (8-11) and OpenGL applications/games under Windows to apply color corrections. DisplayCAL supports generating compatible 3D LUTs (in PNG format) for use with ReShade.

## Requirements

- DisplayCAL (with ArgyllCMS)
- A calibrated display with an ICC profile
- [ReShade](https://reshade.me/) (free and open-source post-processing injector)
- Games or applications that use Direct3D (8-11) or OpenGL
- Check the [ReShade compatibility list](https://reshade.me/forum/general-discussion/87-compatibility-list) for supported games

## Installing ReShade

1. Download the latest version of [ReShade](https://reshade.me/)

2. For ReShade 3.x and newer:
   - The ReShade executable is self-contained
   - Run it and select the game/application executable you want to modify
   - Choose the appropriate rendering API (DirectX or OpenGL)
   - Install the standard effects

3. For ReShade 2.x (older versions):
   - Extract the ZIP file to create a "ReShade <version>" folder
   - Use the "ReShade Mediator" application to configure ReShade for each game

For more information, see the [ReShade website](https://reshade.me/) and [discussion & support forum](https://reshade.me/forum).

## Creating 3D LUTs in DisplayCAL

There are two ways to create 3D LUTs for ReShade:

### Option 1: Create a New Profile and 3D LUT

1. In DisplayCAL, select the "Video 3D LUT for ReShade (Rec. 709 / 1886)" preset under "Settings"

2. On the "Profiling" tab, optionally increase the number of patches with the slider:
   - More patches will yield higher accuracy
   - The default setting should be sufficient for most users

3. On the "3D LUT" tab, adjust settings if needed:
   - Verify "ReShade" is selected as the output format
   - LUT size: 16x16x16, 32x32x32, or 64x64x64 are supported
   - 32x32x32 is recommended for most uses (balance of quality and performance)
   - Source colorspace: "sRGB" for most games (or "Rec. 709" for video content)
   - Target colorspace: Set to your display's profile
   - Rendering intent: "Relative colorimetric" is recommended

4. Click "Calibrate & profile"

5. Adjust the whitepoint of your display if necessary when prompted

6. Wait for measurements and calculations to finish

### Option 2: Create a 3D LUT from an Existing Profile

1. Select the existing profile in DisplayCAL under "Settings"
   - If the profile was created with a 3D LUT, the 3D LUT tab should already be enabled
   - If the tab is grayed out, enable it in the "Options" menu

2. Go to the "3D LUT" tab and:
   - Select "ReShade" under "3D LUT file format"
   - Adjust the lookup table size if desired (16x16x16, 32x32x32, or 64x64x64)
   - Configure any other settings as needed

3. Uncheck "Create 3D LUT after profiling" if it's checked
   - The button at the bottom will change to "Create 3D LUT..."

4. Click "Create 3D LUT..." and wait for the process to finish

## Installing the 3D LUT

When the 3D LUT is created, a window should pop up asking you to install it:

1. Click "Install..."

2. For ReShade 3.x and newer:
   - Choose the folder of the game/application for which you installed ReShade
   - The LUT file should be placed in the same directory as the game executable

3. For ReShade 2.x:
   - Choose your "ReShade <version>" folder

4. Click "Select folder"

5. For ReShade 3.x:
   - Delete the ReShade.fx file in your game folder if it exists from a prior version
   - Use the in-game ReShade configuration menu (default hotkey: HOME)
   - Enable the "LUT" or "Color Lookup Table" effect
   - Configure it to use your PNG file

6. For ReShade 2.x:
   - The 3D LUT should be active by default
   - If not, edit the appropriate configuration files

## Handling 1D Calibration

The ReShade preset is set up to not use 1D calibration by default. However, if you create a ReShade 3D LUT from an existing profile that incorporates 1D calibration or if your display profile uses 1D calibration, you'll need to take extra steps to avoid double-application of calibration.

There are two approaches to handle this:

### Recommended Method: Use DisplayCAL Profile Loader for Exceptions

1. Use DisplayCAL (version 3.1.7 or later) profile loader

2. Right-click the profile loader icon in your system tray

3. Select "Exceptions..."

4. Click "Add..." and browse for the game/application executable

5. Once added, click the gray circle arrow next to the executable name
   - It should turn orange-red
   - This indicates that when the executable is detected, video card gamma tables will be reset
   - They will be automatically restored after the game/application is closed

6. Click "OK" to confirm your changes

7. Ensure your ReShade 3D LUT has calibration applied
   - This is the default setting unless you changed it

While this method requires minimal manual setup, it is the most reliable way to ensure correct calibration.

### Alternative Method: Create 3D LUT Without Calibration

This approach is less recommended because:
- Direct3D applications can override video card gamma tables without notification
- Different gamma tables can be used in windowed vs. fullscreen modes
- It's difficult to verify the actual calibration state while gaming

## Using Multiple LUTs for Different Games

If you play games that use different color spaces or need different display transformations:

1. Create separate 3D LUTs for each color space (e.g., sRGB, Rec.709, P3)
2. Name them clearly (e.g., "game_srgb.png", "game_rec709.png")
3. Configure different ReShade profiles for each game
4. Use the appropriate LUT for each game based on its color characteristics

## 3D LUT Usage

When everything is configured correctly:

1. Launch your game or application

2. You should see a ReShade initialization message in the top left corner

3. A message "Color Look Up Table Shader 1.0" should appear in the center of the screen

4. You can toggle the 3D LUT effect with the HOME key
   - This key can be changed by editing the ColorLookupTable.fx file

5. Use the ReShade overlay (HOME key) to:
   - Adjust LUT strength if desired
   - Toggle individual effects
   - Check performance impact
   - Save your configuration

## Troubleshooting

- **ReShade doesn't initialize:**
  - Verify you're using the correct version of ReShade for your DirectX/OpenGL version
  - Some games require administrative privileges to inject ReShade
  - Try running both the game and ReShade as administrator

- **Can't see the ReShade overlay:**
  - Try other key combinations (Shift+F2, Home, etc. depending on ReShade version)
  - Some games block overlays; check the ReShade compatibility list

- **Colors look incorrect:**
  - Ensure you selected the right source colorspace when creating the LUT
  - Verify the 1D calibration is handled correctly (see "Handling 1D Calibration" section)
  - Try toggling between full and limited RGB range in the 3D LUT settings

- **Anti-cheat issues:**
  - Many online games with anti-cheat systems block ReShade
  - For these games, you may need to use other methods or only use ReShade in offline/single-player mode

- **Performance problems:**
  - Try a smaller LUT size (16x16x16 instead of 32x32x32)
  - Disable other ReShade effects you aren't using
  - Lower your game's resolution or other graphical settings

## Additional Resources

- Return to [Wiki Index](wiki.md)
- [ReShade Documentation](https://reshade.me/docs)
- [Profile Verification Guide](profile-verification.md)
- [DisplayCAL GitHub Repository](https://github.com/eoyilmaz/displaycal-py3)

---

*Last updated: This document is based on information from the original DisplayCAL Wiki (last updated 2017-12-10)* 