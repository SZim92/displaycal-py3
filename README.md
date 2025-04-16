![license](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
![pyversion](https://img.shields.io/pypi/pyversions/DisplayCAL.svg)
![pypiversion](https://img.shields.io/pypi/v/DisplayCAL.svg)
![wheel](https://img.shields.io/pypi/wheel/DisplayCAL.svg)

DisplayCAL Modernization Project
===========================

A modern, actively maintained fork of DisplayCAL (Display Calibration and Characterization) with Python 3 support and enhanced features. DisplayCAL is an advanced open source display calibration and profiling solution.

**Quick Links:**
* [GitHub Repository](https://github.com/eoyilmaz/displaycal-py3)
* [Issue Tracker](https://github.com/eoyilmaz/displaycal-py3/issues)
* [Releases](https://github.com/eoyilmaz/displaycal-py3/releases)

**Current Version: 3.9.15** (See [release notes](https://github.com/eoyilmaz/displaycal-py3/releases) for details)

About This Project
-----------------

Florian Höch, the original developer, did an incredible job of creating and maintaining DisplayCAL for all these years. But, it seems that, during the pandemic, he understandably stepped back from active development. This community-driven fork continues the work by modernizing the codebase for current systems.

This project is based on the ``HEAD`` of the Sourceforge version, which had 5 extra commits that Florian created over the ``3.8.9.3`` release on 14 Jan 2020.

This modernized fork is maintained by [Erkan Ozgur Yilmaz](https://github.com/eoyilmaz) with contributions from the DisplayCAL community. With over 1,000 stars on GitHub, it has become the primary actively maintained version of DisplayCAL.

Key Modernization Features
-------------------------

* **Python 3.8+ Compatibility**: Complete refactoring to support modern Python versions while maintaining the original functionality
* **Enhanced Windows Console Support**:
  * Modern Pseudo Terminal (ConPTY) implementation for reliable Unicode handling on Windows 10 (1809+)
  * Improved stability for interactive command-line tools and scripts
  * Automatic fallback to traditional console handling on older Windows versions
* **Updated Dependencies**: Compatible with current versions of ArgyllCMS and other required libraries

Thanks to all the efforts put by the community, DisplayCAL is now working with Python 3.8+:

![image](screenshots/DisplayCAL-screenshot-GNOME-3.9.5-running_on_python3.10.png)

### Screenshots Gallery

<details>
<summary>Click to view more screenshots</summary>

- [Main DisplayCAL Window](https://displaycal.net/images/DisplayCAL-Main.png)
- [Display Calibration](https://displaycal.net/images/DisplayCAL-calibration.png)
- [Profiling](https://displaycal.net/images/DisplayCAL-profiling.png)
- [Profile Information](https://displaycal.net/images/DisplayCAL-profile-info.png)
- [3D Visualization](https://displaycal.net/images/DisplayCAL-3D.png)
- [Measurement Report](https://displaycal.net/images/DisplayCAL-report.png)

</details>

System Requirements
------------------

* **Python**: 3.8 or newer
* **Operating Systems**:
  * Windows 7 or newer (Windows 10 1809+ recommended for best console experience)
  * macOS 10.13 or newer
  * Linux with X11 or Wayland
* **Dependencies**:
  * ArgyllCMS 2.0.0 or newer
  * wxPython 4.0.0 or newer
  * Additional dependencies listed in requirements.txt

Basic Usage
----------

**Graphical Interface:**
```
python3 -m DisplayCAL
```

**Command Line Profiling:**
```
python3 -m DisplayCAL.main --help
python3 -m DisplayCAL.main --verbose --create-profile
```

For detailed CLI options, see the [documentation](docs/).

Getting Started
--------------

### Basic Display Calibration

1. Connect your colorimeter or spectrometer
2. Launch DisplayCAL
3. Select your instrument and display
4. Choose a calibration target (e.g., sRGB, Rec. 709, custom white point)
5. Click "Calibrate & profile" to start the process

### Command Line Quick Start

Profile a display using the command line:

```bash
# Display available instruments
python3 -m DisplayCAL.main --help-devices

# Profile monitor 1 with default settings
python3 -m DisplayCAL.main --display 1
```

See the [command line documentation](docs/command-line.md) for more advanced options.

Installation Instructions
=========================

Follow the instructions depending on your OS:

- [Windows](docs/install_instructions_windows.md)
- [MacOS](docs/install_instructions_macos.md)
- [Linux](docs/install_instructions_linux.md)

Documentation
============

### User Guides
* [DisplayCAL Wiki](docs/wiki.md)
* [Novice Guide](docs/novice-guide.md)
* [FAQ](docs/faq.md)

### Technical Documentation
* [Command Line Reference](docs/command-line.md)
* [Display Profile Verification](docs/profile-verification.md)

### Installation Guides
* [Windows Installation](docs/install_instructions_windows.md)
* [macOS Installation](docs/install_instructions_macos.md)
* [Linux Installation](docs/install_instructions_linux.md)

Project Status
-------------

This project is actively maintained by [Erkan Ozgur Yilmaz](https://github.com/eoyilmaz) and the community. Our current focus includes:

- Ensuring compatibility with newer Python versions and operating systems
- Fixing bugs and addressing compatibility issues with newer hardware
- Improving usability and documentation
- Maintaining compatibility with the latest color measurement instruments

Recent achievements:
- Added proper Unicode handling in console applications (Windows ConPTY support)
- Fixed compatibility with i1Pro3 colorimeters
- Resolved macOS-specific issues
- Improved stability and reliability

Future plans include a complete UI refresh and additional instrument support.

Contributing
===========

Contributions to this modernization effort are welcome! Please feel free to submit issues and pull requests.

We especially appreciate help with:

- Testing on different platforms and with various instruments
- Documentation improvements
- Code refactoring and modernization
- Translation updates

### Reporting Issues

When reporting issues, please include:

1. Your OS version and Python version
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. For hardware-related issues, please specify your instrument model

### Pull Requests

Pull requests are welcome! Please:

1. Keep changes focused on a single issue or feature
2. Follow the existing code style
3. Add tests for new functionality where possible
4. Update documentation to reflect changes

Supported Hardware
-----------------

DisplayCAL works with a wide range of colorimeters and spectrometers via ArgyllCMS, including:

- X-Rite/Gretag Macbeth (i1Display, i1Pro, ColorMunki, etc.)
- Datacolor (Spyder2, 3, 4, 5, etc.)
- ColorVision
- Hughski ColorHug
- And many others supported by ArgyllCMS

For the full list of supported devices, please refer to the [ArgyllCMS documentation](https://www.argyllcms.com/doc/ArgyllDoc.html).

Acknowledgments
--------------

- Florian Höch for creating and maintaining DisplayCAL for many years
- [Erkan Ozgur Yilmaz](https://github.com/eoyilmaz) for leading this Python 3 modernization project
- ArgyllCMS developers for the underlying color engine
- All community contributors who helped with Python 3 migration
- Everyone who has reported issues and helped with testing

Related Projects
--------------

* [ArgyllCMS](https://www.argyllcms.com/) - The underlying color management engine
* [Colour Science](https://www.colour-science.org/) - Python package for color science applications
* [ColorMine](https://github.com/colormine/colormine) - Color conversion and management library

License
-------

DisplayCAL is licensed under the GNU General Public License v3 (GPL-3.0). See [LICENSE.txt](LICENSE.txt) for details.

Have fun!
