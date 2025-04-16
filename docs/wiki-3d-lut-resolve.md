# 3D LUT Creation Workflow for DaVinci Resolve

This guide explains how to create and use 3D LUTs (Lookup Tables) with DisplayCAL for color management in DaVinci Resolve.

> **IMPORTANT:** When using Resolve 14 or later and an external video monitor, you must **uncheck** "Release video I/O hardware when not in focus" under Resolve preferences -> Video and Audio I/O, otherwise Resolve will not show the patterns it receives via the external monitor! You may restore this preference after all measurements are complete if desired.

## Overview

DisplayCAL can generate highly accurate 3D LUTs that allow you to perform display-referred color transformations in DaVinci Resolve. This is particularly useful for:

- Ensuring accurate color representation on your calibrated display
- Creating consistent color transformations across different systems
- Soft-proofing different output targets (e.g., Rec.709, P3, etc.)

## Requirements

- DisplayCAL (with ArgyllCMS)
- A calibrated display with an ICC profile
- DaVinci Resolve (version 10.1 or newer)
- A colorimeter or spectrophotometer

## Prerequisites

Before beginning the calibration process:

- If using a colorimeter (e.g., i1 DisplayPro, ColorMunki Display, or Spyder 4/5), consider importing vendor spectral corrections for your display type:
  1. Select "Import colorimeter corrections from other software" in the "Tools" menu
  2. Make sure i1Profiler is selected and click the "Auto" button
  3. After importing, these corrections will be listed under "Corrections" on the "Display & instrument" tab
  4. Choose the correction that matches your display technology

## Workflow Options

There are two distinct workflows for creating 3D LUTs in DisplayCAL for Resolve:

1. **Pattern generator workflow** - For displays not part of the desktop (e.g., connected via a DeckLink card)
2. **GUI color viewer workflow** - For displays that are part of the desktop system

Choose the appropriate workflow based on your setup.

## Pattern Generator Workflow (External Display)

This workflow is for creating a 3D LUT for a display that is **not** part of the desktop (e.g., connected via a DeckLink card or similar).

1. In DisplayCAL, choose the "3D LUT for Resolve (D65, Rec. 709 / 1886)" preset under "Settings"

2. If using an OLED, Plasma, or other display with variable light output, enable white level drift compensation

3. Configure measurement patches (optional):
   - The default 1553 patches should give good results
   - More patches increase measurement time and accuracy
   - If needed, reduce the amount of patches in the "Profiling" tab

4. Configure tone curve (optional):
   - The "Resolve" preset is set up to not use iterative gray balance calibration
   - If you want to use iterative gray balance, set calibration tone curve on the "Calibration" tab from "As measured" to "Rec. 1886" (or another desired curve)
   - **Note:** This setting does not influence the 3D LUT tone curve

5. For a different 3D LUT tone curve:
   - Go to the "3D LUT" tab and adjust the options
   - For gamma 2.2 "output offset" curve, set tone curve to "Gamma 2.2"
   - For a blend between input offset (BT.1886) and output offset, set tone curve to "Custom" and output offset between 0% and 100%

6. Adjust the 3D LUT output format and encoding if needed

7. Click "Calibrate & profile"

8. A message "Waiting for connection on IP:PORT" will appear - note the IP and port numbers

9. In Resolve:
   - Switch to the "Color" tab
   - Choose "Monitor calibration" -> "CalMAN" in the "Workspace" menu (or "Color" menu in older versions)
   - Enter the IP address in the window (port should already be filled)
   - Click "Connect"

10. Position the measurement window:
    - Drag to the desired location and size
    - A size just large enough to fit the instrument is usually best
    - The position will be mimicked on your external display after clicking "Start measurement"

11. When prompted by DisplayCAL, place the instrument on the designated spot and click OK

12. Use the interactive display adjustment window to adjust whitepoint and luminance

13. After measurements and calculations complete:
    - A window will show profile self check error and gamut coverage
    - The self check error should not be higher than 0.5 ΔE average and 5 ΔE peak
    - Click "Save 3D LUT..." to save the file to one of Resolve's LUT folders:
      - Windows: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT`
      - macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT`

14. Optional verification:
    - Go to the "Verification" tab and click "Measurement report"
    - Settings should already be correct for the chosen parameters
    - Consider choosing a larger testchart for more thorough examination

## GUI Color Viewer Workflow (Desktop Display)

This workflow is for creating a 3D LUT for the Resolve GUI color viewer on a display that is part of the desktop.

1. In DisplayCAL, choose the "3D LUT for Resolve (D65, Rec. 709 / 1886)" preset under "Settings"

2. Select your actual display device under the display dropdown instead of Resolve

3. If using an OLED, Plasma, or other display with variable light output, enable white level drift compensation

4. Configure measurement patches (optional) in the "Profiling" tab

5. Consider iterative gray balance calibration:
   - The "Resolve" preset is set up to not use iterative gray balance calibration
   - Since the profile will be installed to the OS, you may want to enable it
   - Set calibration tone curve on the "Calibration" tab from "As measured" to "Rec. 1886" (or another desired curve)

6. **IMPORTANT:** If using iterative gray balance calibration:
   - Enable advanced options in the "Options" menu
   - Go to the "3D LUT" tab and **disable** "Apply calibration (vcgt)"
   - This prevents double-application of calibration since Resolve's UI is affected by the system's 1D calibration

7. Configure tone curve and other 3D LUT settings as desired

8. Click "Calibrate & profile"

9. Position the measurement window and click "Start measurement"

10. Use the interactive display adjustment window to adjust whitepoint and luminance

11. After measurements and calculations complete:
    - Save the 3D LUT file to Resolve's LUT folder
    - Go to the "Display & instrument" tab
    - Click the "Install profile" button next to the settings dropdown to install the profile to your system

12. Optional verification:
    - Go to the "Verification" tab and click "Measurement report"
    - Enable the "DeviceLink profile" checkbox

## Using the 3D LUT in Resolve

### For External Displays (Pattern Generator Workflow)

1. Open the "File" menu and select "Project settings..."
2. Select "Color Management" from the list
3. Choose your 3D LUT under the "3D Video Monitor Lookup Table" entry
4. Set your scopes to not use the video monitor selection
5. Optionally set 3D Lookup Table Interpolation to "Tetrahedral" for better accuracy

### For Desktop Displays (GUI Color Viewer Workflow)

1. Open the "File" menu and select "Project settings..."
2. Select "Color Management" from the list
3. Choose your 3D LUT under the "3D Color Viewer Lookup Table" entry
4. Set "Use Mac Display Color Profiles for Viewers" to OFF (macOS only)
5. Optionally set 3D Lookup Table Interpolation to "Tetrahedral" for better accuracy

## Creating Additional 3D LUTs from Existing Measurements

You can create additional 3D LUTs with different settings from any existing profile:

1. Select the desired profile under "Settings"
2. Go to the "3D LUT" tab
3. Disable "Create 3D LUT after profiling"
4. The button at the bottom will change to "Create 3D LUT..."
5. Adjust the 3D LUT settings as needed
6. Click "Create 3D LUT..." to generate a new LUT with these settings

## Troubleshooting

- **High self check errors:** If errors are much higher than 0.5 ΔE average and 5 ΔE peak, try:
  - Increasing the measurement delay (in 50-100ms increments)
  - Enabling white level drift compensation for OLED/Plasma displays
  - Using a spectral correction profile that matches your display technology

- **Connection issues:** When DisplayCAL shows "Waiting for connection on IP:PORT":
  - If connecting on the same machine, use 127.0.0.1 or localhost instead of the displayed IP
  - Check for firewall settings that might block the connection
  - Verify Resolve is in the Color page when attempting to connect

- **Double-applied calibration:** If colors appear washed out or incorrect:
  - Verify "Apply calibration (vcgt)" is disabled in the 3D LUT settings for GUI viewer workflow
  - Ensure "Use Mac Display Color Profiles for Viewers" is OFF when using a 3D Color Viewer LUT

- **Viewer colors don't match on Edit page:** The Color Viewer LUT only applies to the Color page; use the Video Monitor LUT if you need consistent colors throughout Resolve

## Additional Resources

- Return to [Wiki Index](wiki.md)
- [Profile Verification Guide](profile-verification.md)
- [DaVinci Resolve Documentation](https://www.blackmagicdesign.com/products/davinciresolve)

---

*Last updated: This document is based on information from the original DisplayCAL Wiki (last updated 2019-06-12)* 