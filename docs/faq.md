# DisplayCAL Frequently Asked Questions

This document answers common questions about display calibration and profiling with DisplayCAL. If you're new to display calibration, you might want to start with the [Novice Guide](novice-guide.md) first.

## Basic Concepts

### What's the difference between calibration and profiling?

**Calibration** adjusts your display to conform to specific targets (white point, gamma, brightness). It modifies how your display behaves by adjusting the video card's lookup tables (videoLUT).

**Profiling** measures the display's color response and creates an ICC profile that describes how it reproduces color. Applications that support color management use this profile to display colors accurately.

Calibration happens before profiling, and good calibration leads to better profiling results.

### Do I need to calibrate my display?

It depends on your work:
- **Professional photographers, designers, and video editors**: Yes, calibration is essential for accurate color reproduction, especially if you're producing work for print or other media.
- **Casual users**: Not immediately necessary, but it provides a better visual experience.
- **Gaming and entertainment**: Can improve visual experience but isn't critical.

### What equipment do I need?

At minimum:
- A quality display (ideally IPS panel)
- A colorimeter or spectrophotometer (X-Rite i1Display Pro/Studio or Datacolor Spyder series)
- DisplayCAL software

## Hardware and Setup Questions

### Can I use software to adjust RGB gains if my monitor doesn't have hardware controls (e.g., laptop/iMac)?

Generally, no. Software solutions that adjust RGB gains via the video card's gamma tables (videoLUT) conflict with the calibration process. DisplayCAL also uses the videoLUT for calibration, so they cannot be used together.

For displays without hardware controls, you have these options:
- Calibrate with the native white point using "As measured" as the white point target
- Use the visual white point editor in DisplayCAL for a software-based adjustment, but understand this is less ideal than hardware controls

### What displays work best with calibration?

Displays with these features calibrate best:
- IPS, PVA, or AHVA panel technology (avoid TN panels)
- Hardware controls for RGB adjustment (separate red, green, blue controls)
- Wide color gamut coverage (100% sRGB or greater)
- Consistent brightness across the screen
- At least 8-bit color depth

### How long should I warm up my display before calibration?

At least 30 minutes. LCD/LED displays need time to reach stable temperature and brightness levels. For the most accurate results, place your colorimeter on the screen during this warm-up period.

## Calibration Process

### Which correction factors should I choose for my display?

Select the correction that matches your display technology:
- **LCD White LED Family**: For standard displays with white LED backlights (most laptops, desktop LCDs made after 2010)
- **LCD PFS Phosphor WLED Family**: For wide gamut displays with newer LED technology
- **LCD RGB LED**: For displays with RGB LED backlights
- **LCD CCFL**: For older displays with CCFL backlights
- **For Mac users**: Retina displays (2016+) have specific profiles

When in doubt, check your display's specifications or use the information panel in DisplayCAL for guidance.

### What white point target should I use?

Common white point targets:
- **6500K (D65)**: Standard for web content, video editing, and general use
- **5000K (D50)**: Standard for print preparation and soft-proofing
- **Native**: Use "As measured" if you want to maintain your display's native white point

### What brightness (white level) should I target?

Typical recommendations:
- **120 cd/m²**: General purpose use
- **80-100 cd/m²**: Print-focused work
- **160 cd/m²**: Brightly lit environments

Lower values provide better black level detail but can appear too dim in bright rooms.

### What tone curve (gamma) should I use?

- **Gamma 2.2**: Standard for most purposes, including Windows and photo editing
- **sRGB**: For web content and general use (slightly different from pure 2.2)
- **BT.1886**: For video editing and preparation (better shadow performance)

## Multiple Display Questions

### I have two or more displays and have calibrated all of them to the same parameters. Why don't they match visually?

Several factors can cause displays to look different even after calibration:

1. **Different panel technologies**: Various technologies (IPS, VA, TN) have inherently different viewing characteristics and color reproduction.

2. **Different backlight technologies**: LED, CCFL, and other backlights produce different spectral outputs that affect color perception.

3. **Different gamut coverage**: A wide-gamut display and a standard-gamut display can't match perfectly in all colors.

4. **Perception differences**: Human visual perception adjusts to different white points, and viewing angle affects how colors appear.

### How can I make multiple displays match better?

For optimal matching:

1. Choose one display as a reference (ideally your best or primary display).

2. For displays with hardware controls:
   - Display a white patch on all screens
   - Adjust RGB controls on secondary displays to visually match the reference
   - Use "As measured" for white point in DisplayCAL
   - Calibrate and profile each display

3. For displays without hardware controls:
   - Use DisplayCAL's visual white point editor
   - Adjust until displays match visually
   - Click "Measure" to set this as the calibration target
   - Continue with calibration and profiling

4. To match contrast better:
   - Enable advanced options in DisplayCAL
   - Set a black level target on all displays that matches the display with the highest black level

## Troubleshooting

### My colorimeter isn't being detected by DisplayCAL.

Try these solutions:
- Check the USB connection and try a different USB port
- For Datacolor devices: Go to Tools > Instrument > "Install ArgyllCMS instrument drivers"
- Restart DisplayCAL and your computer
- On Windows, check Device Manager to ensure the device is properly recognized
- On Mac, check System Information > USB to verify the device is connected

### The calibration results don't look right. Colors seem off.

Common causes and solutions:
- **Wrong correction profile**: Ensure you've selected the correction that matches your display technology
- **Environment changed**: Lighting conditions affect visual perception
- **Display settings changed**: Check if any automatic brightness/contrast features are active
- **Profile not active**: Verify the profile is set as default for the display
- **Application not using profile**: Ensure your applications are using color management

### DisplayCAL reports high Delta E values after calibration.

High Delta E values can be caused by:
- **Incorrect correction profile**: Try a different correction that better matches your display
- **Display limitations**: Some displays cannot accurately reproduce certain colors
- **Hardware controls at extremes**: If RGB controls are at minimum or maximum, you have limited adjustment range
- **Instrument limitations**: Consumer colorimeters have accuracy limitations
- **Unstable display**: Recalibrate after proper warm-up

### What does "Profile quality" actually change?

Profile quality affects the number of measurements and calculations used to create the profile:
- **Low**: Faster but less accurate
- **Medium**: Good balance between speed and accuracy
- **High**: More accurate but takes longer
- **Very High**: Maximum accuracy, significantly longer processing time

For most users, "High" provides good results without excessive measurement time.

## DisplayCAL-py3 Specific Questions

### What's different in the Python 3 version of DisplayCAL?

DisplayCAL-py3 offers several improvements over the original:
- **Python 3.8+ Compatibility**: Updated codebase works with modern Python versions
- **Enhanced Windows Console Support**: Modern Pseudo Terminal (ConPTY) implementation for reliable Unicode handling on Windows 10 (1809+)
- **Improved Stability**: Better handling of interactive tools and scripts
- **Updated Dependencies**: Compatible with current versions of ArgyllCMS and other required libraries

### Does DisplayCAL-py3 work with Apple Silicon Macs (M1/M2)?

Yes, DisplayCAL-py3 works with Apple Silicon Macs, though there may be occasional issues as the platform evolves. For best results:
- Use the latest version from the [GitHub repository](https://github.com/eoyilmaz/displaycal-py3)
- Install dependencies through a package manager like Homebrew
- Grant necessary permissions in System Preferences > Security & Privacy

### How do I use DisplayCAL with HDR displays?

For HDR displays:
1. Disable HDR mode in your operating system before calibration
2. Calibrate in SDR mode first
3. After calibration, you can enable HDR for content consumption, but understand that the calibration applies primarily to SDR content
4. For advanced HDR calibration, specialized tools beyond standard DisplayCAL may be required

## Advanced Topics

### What profile type should I choose?

DisplayCAL can create different types of ICC profiles:
- **Single curve + matrix**: Smaller, more compatible profile type, works well with well-behaved displays
- **XYZ LUT + matrix**: More accurate for displays with non-linear behavior, but larger files
- **XYZ LUT**: Most accurate but largest file size and potentially less compatible

On macOS, "Single curve + matrix" (34 patches) is recommended for system-wide compatibility.

### Can I use DisplayCAL to create 3D LUTs for video use?

Yes, DisplayCAL can create 3D LUTs for video applications:
1. Go to the "3D LUT" tab after profiling
2. Select your target colorspace (Rec. 709, DCI-P3, etc.)
3. Choose your preferred 3D LUT format (.cube, .3dl, etc.)
4. Configure the rendering intent and other parameters
5. Create the 3D LUT after profiling

### How accurate are consumer colorimeters?

Consumer colorimeters (like i1Display Pro or Spyder series) are generally accurate enough for most uses, with some limitations:
- They're most accurate for the display technologies they were designed for
- Accuracy decreases over time (typically 2-3 years of regular use)
- They're less accurate for very wide gamut displays
- Spectrophotometers are more accurate but significantly more expensive
- Using appropriate correction factors in DisplayCAL greatly improves accuracy