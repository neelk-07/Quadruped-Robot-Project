# Quadruped Robot Controller

A Python-based quadruped robot control system with a GUI Interface to control positions for a quadruped robot. This system allows controlling the robot's servos using a graphical interface, saving and loading robot states, and communication with a microcontroller over serial.

### Important Notes:
This has only been tested with:
- **Visual Studio Code** for the GUI, with Python (tkinter).
- **Thonny** for MicroPython.
- **Raspberry Pi Pico W** microcontroller

**Required hardware:** A quadruped robot with four legs, each with two servos, is required to use this controller.

## Table of Contents
- [Project Title and Description](#project-title-and-description)
- [Installation and Setup Instructions](#installation-and-setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Licenses](#licenses)
- [Libraries](#libraries)

## Project Title and Description
This project is designed to control a quadruped robot using a set of servos. It includes:
- A GUI to control the servo positions.
- The ability to save and load robot states.
- Communication with a Raspberry Pi Pico W via serial.

## Installation and Setup Instructions
1. Clone this repository:
```bash
git clone https://github.com/Heli202/Quadruped-Robot-Controller
```
2. Install/Setup Dependencies:
- Ensure Python and MicroPython is installed on your system.
- Tkinter should be installed by default with Python, if not it will need to be installed separately.
- Install the required dependencies (`pyserial`) listed in `requirements.txt` for both VSCode and Thonny.
```bash
pip install -r requirements.txt
```

3. Setup microcontroller environment:
- Connect the microcontroller to your PC via USB.
- Open Thonny, then go to **Tools > Options > Interpreter** and select MicroPython (Raspberry Pi Pico) for the interpreter. Then select the appropriate COM port for your microcontroller from the list (you can check the assigned COM port in the **Device Manager** on Windows).
- Flash MicroPython onto the microcontroller if it's not already installed.

4. Transfer necessary files to the microcontroller in Thonny:
- Upload the `Quadruped_Thonny.py` file onto the microcontroller's filesystem. This file contains the main program logic for receiving commands from the GUI.

5. Using Thonny to start the microcontroller main loop:
- To start the main loop, after the `>>>` type:
```bash
import Quadruped_Thonny
```
- Once the `>>>` appears again type:
```bash
Quadruped_Thonny.start()
```
- `Starting main loop...` will now appear.
- Now close Thonny, while keeping the microcontroller plugged in.
6. Open the GUI:
- Open `Quadruped_PC` to launch the GUI.
## Usage Instructions
- From the GUI you now have the following controls:
### Scale Controls
- Control the **Scales** to adjust the degrees for servo movement.
- `Reset Scales` to reset all Scales to 0.
### State Control
- `Save State` and `Load State` buttons allow you to save and load configurations, with entry fields for naming each state.
### Command Control
- `Send to Pico` sends a command via serial communication to the Raspberry Pi Pico W, which adjusts the servo positions accordingly.

### Demo Video (showcasing functionality):
![Demo Video](https://img.youtube.com/vi/hOMUS9vagQ8/0.jpg)

[Watch the video](https://youtu.be/hOMUS9vagQ8)

## Licenses
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Libraries

### External Libraries
This project uses the following external libraries:
- **PySerial** - Check their [Repository](https://github.com/pyserial/pyserial) for more info.
  - License: [PSF License](https://opensource.org/license/python-2-0)

### Standard Libraries
#### Python
- **tkinter** - used for GUI development (Standard Library in Python, governed by Python's PSF License).
- **sys** - for interacting with the Python runtime environment (Standard Library in Python, governed by Python's PSF License).
- **json** - for working with JSON data (Standard Library in Python, governed by Python's PSF License).
#### MicroPython
- **machine** - used for controlling hardware components (e.g. GPIO, PWM) (Standard Library in MicroPython, governed by the MIT License).
- **sockets** - for network communication using the socket API in MicroPython (Standard Library in MicroPython, governed by the MIT License).
- **time** - for handling time-related functions (Standard Library in MicroPython, governed by the MIT License).
