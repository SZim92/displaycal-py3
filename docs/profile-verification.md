# DisplayCAL Profile Verification Guide

Profile verification is an essential feature in DisplayCAL that allows you to measure how well your display performs compared to a reference standard or your calibration targets.

## Overview

Verification in DisplayCAL serves several key purposes:
- Validating the accuracy of a display calibration
- Checking how closely your display matches standard color spaces (sRGB, Adobe RGB, etc.)
- Comparing the performance of different display profiles
- Assessing your display's native color accuracy

## Verification Workflow

### Basic Verification Steps

1. Launch DisplayCAL
2. Select the appropriate settings for your verification needs
3. Click "Measurement Report" to start the verification process
4. Review the resulting report to assess color accuracy

### Common Use Cases

#### Use Case 1: Verifying a DisplayCAL Calibration Profile

To check how accurately your monitor performs with your calibration profile:

1. In DisplayCAL, select your calibration profile from the "Settings" dropdown
2. Select "Verification testchart" under "Testchart"
3. Enable "Simulation profile" and select a reference (typically sRGB for standard work)
4. Ensure "Use simulation profile as display profile" is **unchecked**
5. Click "Measurement report"

This tests how well your calibrated display shows colors from the reference profile space.

#### Use Case 2: Testing Native Display Performance

To check how your display performs with its factory/default settings:

1. In "Settings" dropdown, select your DisplayCAL profile
2. Select "Verification testchart" under "Testchart"
3. Enable "Simulation profile" and select your current display profile
4. Check "Use simulation profile as display profile"
5. Set "Tone curve" to "Unmodified"
6. Click "Measurement report"

This tests how accurately your uncalibrated display performs.

## Understanding Options

### Settings Dropdown
The profile loaded here provides the calibration data for measuring against. For verifying a DisplayCAL calibration, select your profile here.

### Simulation Profile
This is the reference standard your measurements will be compared against. Common choices include:
- sRGB for web content and general work
- Adobe RGB for print work
- Rec. 709 for video work
- Your display's own profile to test native accuracy

### "Use simulation profile as display profile"
- **Checked**: Tests how the display performs with the simulation profile assigned as the active display profile.
- **Unchecked**: Tests how the display renders content from the simulation profile's color space while using your selected profile.

### Tone Curve Options
- **Apply black output offset**: Applies the same black point compensation as during calibration
- **Unmodified**: Uses the curve exactly as defined in the profile

## Interpreting Results

The verification report provides essential metrics:

- **ΔE (Delta E)**: Color difference measurements - lower values are better
  - ΔE < 1.0: Excellent, imperceptible difference
  - ΔE < 2.0: Good, barely perceptible
  - ΔE < 3.5: Acceptable for most purposes
  - ΔE > 3.5: Noticeable difference
- **Gamut coverage**: How much of the reference colorspace your display can show
- **White point accuracy**: How closely your white matches the target
- **Tone response**: How accurately your display follows the gamma curve

## Platform-Specific Notes

### macOS
- On macOS, the "<Current>" option in the settings dropdown may not allow verification without a simulation profile
- To test a non-DisplayCAL profile, you may need to:
  1. Use File > Install Display Profile to install the profile
  2. Select it as a simulation profile
  3. Check "Use simulation profile as display profile"

### Windows
- The "Use simulation profile as display profile" option is particularly useful for testing non-color-managed applications

## Troubleshooting

- If "Measurement Report" is greyed out, ensure you have a valid profile selected
- For macOS users, if the default profile can't be verified directly, try "File > Generate ICC from Extended Display Data (EDID)"
- If verifying a 3rd-party profile fails, it may not contain the necessary color information for verification

## Advanced Usage

For in-depth display verification, consider:
- Using larger test charts (more patches give more accurate results)
- Testing specific color regions important to your work
- Comparing multiple profiles to find the best one for your needs
- Testing different display settings (brightness, contrast, etc.)
