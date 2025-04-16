# DisplayCAL Novice Guide

## Introduction

DisplayCAL (Display Calibration and Characterization) is an advanced open-source display calibration and profiling solution. This novice guide will help you get started with the basic workflow for calibrating your display, ensuring color accuracy for photography, design, and other visual work.

## Should You Calibrate Your Display?

While everyone benefits from accurate colors, display calibration is especially important for:

- **Professional photographers**: Essential for client work, especially when photos will be printed
- **Graphic designers**: Ensures your designs appear as intended across different media
- **Video editors**: Helps maintain consistent colors throughout production
- **Photo enthusiasts**: Improves editing quality and consistency

Casual users who don't work with visual media professionally might not need calibration immediately, but it's still beneficial for an improved viewing experience.

## What You'll Need

1. **A quality display**: Ideally an IPS panel (avoid TN panels which have poor viewing angles)
2. **A colorimeter or spectrophotometer**: Such as X-Rite i1Display Pro/Studio or Datacolor Spyder series
3. **DisplayCAL software**: The software you're currently using

## Installation

1. **Install DisplayCAL**:
   - Windows: Follow the [Windows installation guide](install_instructions_windows.md)
   - macOS: Follow the [macOS installation guide](install_instructions_macos.md)
   - Linux: Follow the [Linux installation guide](install_instructions_linux.md)

2. **First Launch**:
   - DisplayCAL will prompt you to download ArgyllCMS, the underlying engine for calibration
   - Allow this download to complete
   - On macOS, you may need to grant necessary permissions for screen recording and disk access

## Preparing for Calibration

For optimal results, follow these preparation steps:

1. **Warm up your display** for at least 30 minutes before calibration
2. **Disable adaptive features** like automatic brightness adjustment, night shift, blue light filters
3. **Reset your monitor** to factory defaults if you've previously changed settings
4. **Clean your screen** to remove dust and fingerprints
5. **Control your environment**:
   - Reduce direct light falling on the screen
   - Maintain consistent room lighting (ideally dimmer than normal office lighting)

## Basic Calibration Workflow

### Step 1: Configure Display & Instrument Settings

1. Launch DisplayCAL
2. On the **Display & instrument** tab:
   - **Display**: Select your display from the dropdown
   - **Instrument**: Your colorimeter should appear automatically
   - **Mode**: Select "LCD (generic)" for most modern displays
   - **Correction**: Choose the appropriate spectral correction:
     - "LCD White LED Family" for standard displays (including most laptops)
     - "LCD PFS Phosphor WLED Family" for wide gamut displays
     - For Mac users: Retina displays (2016+) have specific profiles

![DisplayCAL Display & instrument tab](docs/images/displaycal-display-instrument-tab.png)

### Step 2: Configure Calibration Settings

On the **Calibration** tab:

1. **Interactive display adjustment**: Keep enabled for first-time calibration
2. **White point**: Set to "Color temperature" and choose:
   - 6500K: Standard for web/screen content (D65)
   - 5000K: For print work (D50)
3. **White level**: Set to "Custom" and choose:
   - 120 cd/m²: General purpose setting
   - 90-100 cd/m²: For print-focused work (less bright)
4. **Tone curve**: Use "Gamma 2.2" for most purposes
5. **Calibration speed**: "High" is sufficient for most users

### Step 3: Configure Profiling Settings

On the **Profiling** tab:

1. **Profile quality**: Set to "High"
2. **Testchart**: Keep at "Auto-optimized"
3. **Amount of patches**:
   - Windows: 175 patches recommended
   - Mac: 34 patches (important for macOS compatibility)
4. **Profile name**: Default setting is usually fine

### Step 4: Position Your Colorimeter

1. Place the colorimeter at the center of your screen
2. Make sure it's flat against the display surface
3. Use the counterweight to stabilize the device
4. Shield the colorimeter from direct light if possible

### Step 5: Run the Calibration

1. Click the **Calibrate & profile** button
2. If prompted, adjust your monitor's hardware controls:
   - Brightness/contrast (to match target white level)
   - RGB controls (if available, to match target white point)
3. After adjustments, click **Continue on to calibration**
4. The calibration process will run (10-30 minutes)
5. When complete, install the profile as system default

## Understanding Results

After calibration, you'll see a summary screen with key performance metrics:

- **Delta E values**: Lower is better, under 2.0 is considered good
- **Gamut coverage**: Shows what percentage of standard color spaces your display can show
- **Tone response**: How well your display follows the gamma curve
- **White point accuracy**: How close your white point is to the target

## Verification

To verify your calibration:

1. Go to the **Verification** tab
2. Select "Extended verification testchart"
3. Click **Measurement report**
4. Review the results:
   - Green values indicate good calibration
   - Red values may indicate areas that need improvement

See the [Profile Verification Guide](profile-verification.md) for detailed information.

## When to Recalibrate

Displays change over time. Consider recalibrating:

- Every 1-3 months for professional work
- When you notice color shifts
- After changing display settings
- After driver or system updates

## Troubleshooting

### Colorimeter Not Detected

- Ensure it's properly connected
- Try a different USB port
- For Datacolor devices: Go to Tools > Instrument > "Install ArgyllCMS instrument drivers"

### Mac-Specific Issues

- For M1/M2 Macs: Use the latest version from the [DisplayCAL-py3 repository](https://github.com/eoyilmaz/displaycal-py3)
- Grant necessary permissions in System Preferences > Security & Privacy

### Windows-Specific Issues

- DisplayCAL-py3 includes modern Pseudo Terminal (ConPTY) implementation for better Unicode support on Windows 10 (1809+)
- Improved stability for interactive console applications
- If using multiple GPUs, ensure your display is connected to the GPU that's set as primary

### Poor Calibration Results

- Try a different correction profile
- Ensure your environment is consistently lit
- Check that all adaptive brightness features are disabled
- Reset monitor to factory defaults and try again

## Advanced Features

Once you're comfortable with basic calibration, explore:

- Custom test charts for specific color ranges
- 3D LUT creation for video applications
- Profile verification against industry standards
- Multiple display matching

## Additional Resources

- [Command Line Reference](command-line.md)
- [Profile Verification Guide](profile-verification.md)
- [DisplayCAL-py3 GitHub Repository](https://github.com/eoyilmaz/displaycal-py3)
