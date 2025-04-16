# Setting Up Untethered

This guide explains how to set up DisplayCAL in an untethered configuration, allowing you to use the measurement device on a different computer than the one running DisplayCAL.

> **IMPORTANT:** The untethered mode should generally only be used if you've exhausted all other options. Measurement runs in untethered mode (especially "Auto" mode) will typically take at least twice as long as other methods, and setting it up correctly can be tricky.

## Overview

Normally, DisplayCAL and the measurement device (colorimeter or spectrophotometer) run on the same computer. However, there are scenarios where you might want to:

- Calibrate a display that's connected to a computer with limited processing capabilities
- Calibrate a system without installing DisplayCAL on it
- Calibrate a specialized system where installation of additional software is restricted
- Measure a display that's physically distant from your main workstation

The untethered setup addresses these scenarios by separating the measurement and processing components.

## Requirements

- Two computers:
  - **Control computer**: Runs DisplayCAL and controls the process
  - **Target computer**: Connected to the display being measured
- A colorimeter or spectrophotometer supported by ArgyllCMS
- Network connectivity between the two computers (optional, but helpful)
- ArgyllCMS installed on both computers

## Step-by-Step Setup

### 1. Prepare the Target Computer

1. Install ArgyllCMS on the target computer (the one connected to the display to be measured)
2. Create a folder to store measurement patches and results (e.g., `C:\DisplayCAL_Untethered` or `~/DisplayCAL_Untethered`)
3. Ensure the folder is accessible from the control computer (via network share, USB drive, etc.)

### 2. Configure DisplayCAL on the Control Computer

1. Launch DisplayCAL on the control computer
2. Go to File > Preferences > Advanced
3. Check "Enable untethered measurements"
4. Configure the following settings:
   - **Patch generation method**: Choose how measurement patches will be displayed
   - **Measurement file handling**: Configure how measurement files will be exchanged

### 3. Start the Calibration Process

1. Configure your calibration settings as normal in DisplayCAL
2. When you click "Calibrate" or "Profile", DisplayCAL will:
   - Generate measurement patches
   - Export these to the shared folder
   - Wait for measurement results

### 4. Display and Measure Patches on the Target Computer

1. On the target computer, use a patch display tool to show the measurement patches
   - You can use ArgyllCMS's `dispwin` tool for this purpose
   - Example: `dispwin -c /path/to/patches.ti1`

2. Position your measurement device on the target display
3. Run the measurement tool to measure the displayed patches
   - Using ArgyllCMS's `spotread` tool
   - Example: `spotread -v -d /path/to/patches.ti1 -o /path/to/results.ti3`

4. When measurements are complete, save the results file to the shared folder

### 5. Complete the Calibration

1. Return to DisplayCAL on the control computer
2. DisplayCAL will detect the measurement file and continue the calibration process
3. Follow the remaining steps as in a normal calibration
4. When complete, transfer the resulting ICC profile to the target computer and install it

## Using Untethered "Auto" Mode

For situations where manual patch advancement isn't feasible, DisplayCAL offers an "Auto" measurement mode that automatically detects patch changes. This mode requires careful configuration.

> **Note:** "Auto" testchart mode cannot be used in conjunction with untethered "Auto" measurement mode.

### Understanding How Auto Mode Works

The untethered "Auto" measurement mode:
- Takes at least two readings per patch
- Looks at changes in lightness, hue, and chroma to determine if the patch has changed
- Requires knowledge of the instrument's integration times for your specific display

### Determining Integration Times

Before using "Auto" mode, you need to measure how long your instrument takes to read white and black patches:

1. In DisplayCAL, enable untethered mode but disable the "Auto" measurement mode:
   - Open the "Untethered measures" window
   - Uncheck the "Auto" measurement mode checkbox

2. Measure integration times:
   - Display a black patch on the target screen
   - Click "Measure" (any patch selection will work)
   - Use a stopwatch to note the time it takes to complete the measurement
   - Repeat the process with a white patch
   - Re-enable the "Auto" checkbox and close the "Untethered measures" window

### Preparing Your Testchart

To optimize for automatic patch detection:

1. Open the testchart editor for your selected chart
2. From the "Sort by..." dropdown, select "Maximize lightness difference"
3. Click "Apply"
4. Save the testchart and select "Yes" when asked to use it

### Exporting Patch Images

1. Click "Export" in DisplayCAL
2. Choose an image file format (DPX, PNG, or TIFF) 
3. Click "Save"
4. Set appropriate "max repeat" and "min repeat" values based on your measured integration times:
   - "max repeat" is for black patches (slowest to measure)
   - "min repeat" is for white patches (fastest to measure)
   
   Example calculation:
   - If black patches take 6 seconds to measure and white patches take 1 second
   - At 1 fps playback rate, set "max repeat" to at least 12 (6 × 2) and "min repeat" to at least 2 (1 × 2)
   - Add a safety margin: set "max repeat" to 16 and "min repeat" to 3
   
5. Click "OK" to export the image files

### Measuring with Auto Mode

1. Start the measurement process in DisplayCAL
2. Show the first exported image file on the target display
3. Click "Measure" to start continuous measurement mode
4. Begin playing back all image files on the target display in ascending filename order
5. Auto mode will detect patch changes and record measurements automatically

## Advanced Configuration

### Automation Options

For a more streamlined workflow, you can:

1. Create batch scripts or shell scripts to automate the measurement process
2. Use remote desktop software to control both computers from a single location
3. Set up network-accessible shared folders for automatic file transfers

### Security Considerations

When setting up an untethered configuration:

- Ensure the shared folders have appropriate permissions
- Be cautious about network security if transferring files across networks
- Keep measurement files and profiles in a secure location

## Troubleshooting

- **Auto mode not detecting patch changes**: Increase the "max repeat" and "min repeat" values
- **Communication issues**: Verify that both computers can access the shared folder
- **Measurement errors**: Ensure the measurement device is properly positioned and stable
- **File format problems**: Verify that ArgyllCMS versions are compatible on both systems
- **Display timing issues**: For some displays, you may need to add delays between patches

## Additional Resources

- Return to [Wiki Index](wiki.md)
- [DisplayCAL Command Line Reference](command-line.md)
- [ArgyllCMS Documentation](https://www.argyllcms.com/doc/ArgyllDoc.html)

---

*Last updated: This document is based on information from the original DisplayCAL Wiki (last updated 2018-02-20)* 