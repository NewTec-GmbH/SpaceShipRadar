# SpaceShipRadar - Localization of mobile robots via OpenCV <!-- omit in toc -->

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![CI](https://github.com/NewTec-GmbH/SpaceShipRadar/actions/workflows/test.yml/badge.svg)](https://github.com/NewTec-GmbH/SpaceShipRadar/actions/workflows/test.yml)

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [SW Documentation](#sw-documentation)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Overview

>TODO

## Installation

>TODO
```pip install opencv-contrib-python```
```pip install keyboard```
```pip install numba```
```pip install m2r```
<!-- ```pip install PyQt5``` -->

```bash
git clone https://github.com/NewTec-GmbH/SpaceShipRadar.git
cd SpaceShipRadar
pip install .
```

## Usage

>TODO

### Setup .env
1. Rename the File:

Locate the file named template.env in your project directory.
Rename this file to .env. This is important as the application will look for this specific filename.

2. Adjust the Paths:

Open the newly renamed .env file in a text editor.
You will see several lines that specify paths. You need to update these paths to point to the correct locations on your system.

3. Set the Path for RadonUlzer Executable:

Find the line that starts with RadonUlzer_PATH=.
Change it to reflect the absolute path where program.exe is located on your machine. For example:

RadonUlzer_PATH=C:\path\to\your\LineFollowerSim\program.exe

4. Set the Path for Space Ship Radar Script:

Locate the line starting with SpaceShipRadar_PATH=.
Update it with the absolute path to space_ship_radar.py which is in this repo under ```src\space_ship_radar\```. For example:

SpaceShipRadar_PATH=C:\path\to\your\SpaceShipRadar\src\space_ship_radar\space_ship_radar.py


5. Set the Path for Image Folder:

Find the line that begins with ImageFolder_PATH=.
Ensure this points to the folder containing images (found in this repo under ```src\```), and make sure it ends with a backslash '\\'. For example:

ImageFolder_PATH=C:\path\to\your\src\img\

6. Save Your Changes:

After updating all necessary paths, save and close the .env file.


### Start Script

If webots if open, you can use the start script:

```.\start.ps1```

This will load the RadonUlzer Program specified .env and also load the SpaceShipRadar

<!-- ```bash
template_python [-h] [-v] {command} {command_options}
``` -->

<!-- Detailed descriptions of arguments -->

## Examples

Check out the all the [Examples](./examples).

## SW Documentation

More information on the deployment and architecture can be found in the [documentation](./doc/README.md)

For Detailed Software Design run `$ /doc/detailed-design/make html` to generate the detailed design documentation that then can be found
in the folder `/doc/detailed-design/_build/html/index.html`

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

| Library | Description | License |
| ------- | ----------- | ------- |
| [toml](https://github.com/uiri/toml) | Parsing [TOML](https://en.wikipedia.org/wiki/TOML) | MIT |

see also [requirements.txt](requirements.txt)

---
Sections below, for Github only

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/SpaceShipRadar/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/SpaceShipRadar/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
