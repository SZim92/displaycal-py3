# DisplayCAL Command Line Reference

DisplayCAL offers powerful command-line functionality for automating display calibration and profiling tasks.

## Basic Usage

The main DisplayCAL command-line interface can be accessed using:

```bash
python -m DisplayCAL.main [options]
```

## Common Options

| Option | Description |
|--------|-------------|
| `--help` | Display help information |
| `--help-devices` | List available measurement devices |
| `--display <number>` | Select display to calibrate (1, 2, etc.) |
| `--verbose` | Enable verbose output |

## Calibration & Profiling

| Option | Description |
|--------|-------------|
| `--calibrate` | Perform display calibration only |
| `--create-profile` | Create a display profile (after calibration) |
| `--measurement-mode <mode>` | Set the measurement mode |
| `--whitepoint <x,y>` or `<temperature>` | Set target whitepoint |
| `--luminance <value>` | Set target luminance in cd/m² |
| `--gamma <value>` | Set target gamma |
| `--black-output-offset <value>` | Set black output offset (0-1) |
| `--interactive` | Enable interactive mode (prompts user when needed) |

## Profile Settings

| Option | Description |
|--------|-------------|
| `--profile-type <type>` | Set profile type (e.g., 'S', 'L', 'X', 'G') |
| `--profile-quality <quality>` | Set profile quality ('l', 'm', 'h', 'u' for low, medium, high, ultra) |
| `--profile-name <name>` | Set the profile name |
| `--observer <observer>` | Set the observer (2° or 10°) |

## Input/Output

| Option | Description |
|--------|-------------|
| `--cal <filename>` | Load calibration settings from file |
| `--ti1 <filename>` | Use custom test chart (ArgyllCMS .ti1 file) |
| `--ti3 <filename>` | Use existing measurements file |
| `--output-path <path>` | Set output directory for created files |

## Examples

### Basic Display Calibration

```bash
# Display available instruments
python -m DisplayCAL.main --help-devices

# Calibrate the first display with default settings
python -m DisplayCAL.main --display 1 --calibrate

# Create a profile using specific settings
python -m DisplayCAL.main --display 1 --whitepoint 6500 --gamma 2.2 --luminance 120 --create-profile
```

### Using Existing Measurements

```bash
# Create a profile from existing measurements
python -m DisplayCAL.main --ti3 measurements.ti3 --create-profile
```

### Automating Workflows

```bash
# Fully automated calibration and profiling
python -m DisplayCAL.main --display 1 --whitepoint 6500 --gamma 2.2 --luminance 120 --profile-quality h --create-profile
```

## Advanced Usage

For more advanced command-line features, see the [DisplayCAL Wiki](https://displaycal.net/wiki/) or the original documentation at [displaycal.net](https://displaycal.net/).

You can also check the built-in help for the most up-to-date options:

```bash
python -m DisplayCAL.main --help
``` 