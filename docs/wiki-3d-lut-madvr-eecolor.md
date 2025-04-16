# 3D LUT Creation Workflow for madVR or eeColor

This guide explains how to create and use 3D LUTs (Lookup Tables) with DisplayCAL for high-quality video playback with madVR or eeColor devices.

## Overview

DisplayCAL can generate accurate 3D LUTs that allow you to implement proper color management in madVR (a high-quality DirectShow video renderer) and eeColor (a hardware processor for home theater systems). This ensures that video content is displayed correctly on your calibrated display.

## Requirements

- DisplayCAL (with ArgyllCMS)
- A calibrated display with an ICC profile
- For madVR: A Windows PC with madVR installed
- For eeColor: An eeColor hardware processor
- A colorimeter or spectrophotometer

## Prerequisites

Before beginning the 3D LUT creation process:

- If using a colorimeter that supports it (e.g., i1 DisplayPro, ColorMunki Display, or Spyder 4/5), import and use spectral corrections for your display type:
  1. Select "Import colorimeter corrections from other software" in the "Tools" menu
  2. Make sure i1Profiler is selected and click the "Auto" button
  3. After importing, these corrections will be listed under "Corrections" on the "Display & instrument" tab
  4. Choose the correction that matches your display technology if possible

## Step-by-Step Workflow

### 1. Configure DisplayCAL Settings

1. In DisplayCAL, choose the appropriate preset under "Settings":
   - For madVR: Select "3D LUT for madVR (D65, Rec. 709 / 1886)"
   - For eeColor: Select "3D LUT for eeColor (D65, Rec. 709 / 1886)"

2. If using an OLED, Plasma, or other display with variable light output depending on picture content, enable white level drift compensation

3. Configure measurement patches (optional):
   - The default 1553 patches should already give good results
   - More patches increase measurement time and accuracy
   - If needed, reduce the amount of patches in the "Profiling" tab

4. Configure tone curve (optional):
   - The presets are set up to not use iterative gray balance calibration
   - If you want to use iterative gray balance, set calibration tone curve on the "Calibration" tab from "As measured" to "Rec. 1886" (or another desired curve)
   - **Note:** This setting does not influence the 3D LUT tone curve

5. For a different 3D LUT tone curve:
   - Go to the "3D LUT" tab and adjust the options as desired
   - For gamma 2.2 "output offset" (pure power) curve, set tone curve to "Gamma 2.2"
   - For a blend between input offset (BT.1886) and output offset, set tone curve to "Custom" and output offset between 0% and 100%

6. The 3D LUT output format and encoding are already configured correctly by the preset and usually don't need to be changed

### 2. Start the Calibration and Profiling Process

1. Click "Calibrate & profile"

2. For measurement window setup:
   - For madVR: madTPG (madVR test pattern generator) should start automatically
     - Use the sliders on the madTPG window to adjust patch size and background
   - For eeColor: Drag the measurement window to the desired location and size
   - In both cases, use a patch size just large enough to fit the instrument comfortably

3. Click "Start measurement"

4. If desired, use the interactive display adjustment window to adjust whitepoint and luminance before proceeding, or click "Continue on to calibration/profiling"

5. Wait for the measurements and profile calculations to complete

### 3. Install and Implement the 3D LUT

After measurements and calculations are finished:

1. A window will appear showing profile self check error and gamut coverage:
   - The self check error should not be higher than 0.5 ΔE average and 5 ΔE peak
   - Higher values may indicate measurement issues or display limitations

2. For madVR:
   - Click "Install 3D LUT" to install and activate the 3D LUT directly
   - The 3D LUT will be automatically configured in madVR

3. For eeColor:
   - Click "Save 3D LUT..." to save the file
   - Use the eeColor tools to upload the 3D LUT to the device
   - Follow the eeColor device-specific instructions for implementation

### 4. Verify Your 3D LUT

To verify the quality of your 3D LUT:

1. Go to the "Verification" tab in DisplayCAL
2. Click the "Measurement report" button
3. The settings should already be correct for your chosen 3D LUT parameters
4. You may want to choose a larger testchart for more thorough examination
   - The default chart has only 26 patches and is suitable for a quick check
   - Larger charts provide more comprehensive verification

## Creating Additional 3D LUTs from Existing Measurements

You can create multiple 3D LUTs with different settings from the same measurements:

1. Select an existing profile under "Settings" in DisplayCAL
2. Go to the "3D LUT" tab
3. Disable "Create 3D LUT after profiling"
4. The button at the bottom will change to "Create 3D LUT..."
5. Adjust the 3D LUT settings as needed (tone curve, output format, etc.)
6. Click "Create 3D LUT..." to generate a new LUT with these settings
7. Repeat as needed with different settings

## RGB Range Settings and Troubleshooting

### For madVR

1. Ensure the RGB range settings in madVR match your display's expectations:
   - For most video content, use "Limited Range RGB (16-235)"
   - For PC/Full Range displays, set output to "Full Range RGB (0-255)"
   - Make sure the same range is set in your display settings

2. If the image appears washed out or has crushed blacks:
   - Check for mismatches between input and output RGB ranges
   - Verify that you're not double-applying the calibration

### For eeColor

When creating 3D LUTs for eeColor, pay special attention to RGB range settings:

1. Common configurations to try if you experience washed out images:
   - PC: 0-255 + madVR: 16-235 + projector: 16-235
   - PC: 0-255 + madVR: 0-255 + projector: 0-255
   - PC: 16-235 + madVR: 0-255 + projector: 16-235
   - PC: 16-235 + madVR: 16-235 + projector: 16-235

2. For each PC/madVR/projector configuration, try these 3D LUT file settings:
   - Input: 16-235 + Output: 16-235
   - Input: 0-255 + Output: 0-255
   - Input: 16-235 + Output: 0-255
   - Input: 0-255 + Output: 16-235

3. If you experience persistent issues:
   - Check your actual display contrast ratio (Tools → Report on uncalibrated display)
   - Verify that you're using the correct tone curve for your display technology

## Additional Resources

- Return to [Wiki Index](wiki.md)
- [Profile Verification Guide](profile-verification.md)
- [madVR Official Website](http://madvr.com/)
- [eeColor Documentation](http://eecolor.com/) (if still available)

---

*Last updated: This document is based on information from the original DisplayCAL Wiki (last updated 2016-02-01)* 