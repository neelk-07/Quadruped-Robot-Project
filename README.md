# Quadruped Robot Project [Neel Kumar]

A Python-based control system for a quadruped robot featuring a graphical user interface (GUI) to manage the positions angles of the robot's servos. This system lets users to control the servos, save and load different robot states and to communicate with a microcontroller using serial communication.

### Important Info:
This has only been tested with:
- **Visual Studio Code** for the GUI, with Python (import modules including tkinter, json and pyserial).
- **Thonny** for MicroPython.
- **Raspberry Pi Pico W** microcontroller

**Required hardware:** A quadruped robot with four legs each with a servos at the "knee" and "hip", a **Raspberry Pi Pico W** with a board, a **Micro-USB Connector** and **8 Servo Extension Wires**.

## Table of Contents
- [Project Title and Description](#project-title-and-description)
- [Installation and Setup](#installation-and-setup)
- [GUI Usage Instructions](#GUI-usage-instructions)
- [Licenses](#licenses)
- [Libraries](#libraries)

## Project Title and Description
This project is designed to control a quadruped robot using a set of servos. It includes:
- A GUI to control the servo positions.
- The ability to save and load robot states.
- Communication with a Raspberry Pi Pico W via serial.

## Installation and Setup 
1. Clone this repository:
```bash
git clone https://github.com/neelk-07/Quadruped-Robot-Project.git
```
2. Install/Setup Dependencies:
- Ensure Python and MicroPython is installed on your system.
- The only external module should be `pyserial` which is listed in `requirements.txt` for both VSCode and Thonny.
```bash
pip install -r requirements.txt
```
3. Setup microcontroller environment:
- Connect the microcontroller to your PC via USB.
- Open Thonny, then go to **Tools > Options > Interpreter** and select MicroPython (Raspberry Pi Pico) for the interpreter. Then select the appropriate COM port for your microcontroller from the list (you can check the assigned COM port in the **Device Manager** on Windows).
  
4. Upload the `Quadruped_Thonny.py` file onto the microcontroller's filesystem. This file contains the main program logic for receiving commands from the GUI.

5. Once the file is saved onto the Pico Pi, hit run on Thonny and you should see the shell say `Starting main loop...`. Once loop has started, close Thonny, still keeping the microcontroller plugged in.

6. Open the GUI:
- With VSCode, select the "Open Folder" option, locate the cloned folder location and select the folder. A trust author option should appear so click yes. Now, in VSCode with the folder opened, locate the `Quadruped_PCSide.py` and open it. This is where the GUI can be run. Now hit the run button and the Tkinter based GUI should appear.
## GUI Usage Instructions
### Robot Leg Sliders
- There will be a slider 0-180 for each servo with a label on its left stating which servo each slider corresponds to. You can adjust the slider with the slider handle or by entering a specific value into the entry fields next to the sliders for precision (entered number must be within 0-180).
### State Control
- `Save State` and `Load State` buttons allow you to save and load configurations, with entry fields for naming each state.
### Command Control
- The `Update Pico` sends a command via serial communication to the Raspberry Pi Pico W, which adjusts the servo positions to the position the sliders are set to at that point. There is also a "Stand" button which is a preset to set all servos to the correct position to make the robot stand.

### Demo Video (showcasing functionality):
[Watch the video](https://www.youtube.com/shorts/xikzhpxLIr0)

## Licenses
This project is licensed under the MIT and PSF Licenses

## Libraries
### External Libraries
This project uses the following external libraries:
- **PySerial** - Check their [Repository](https://github.com/pyserial/pyserial) for more info.
  - License: [PSF License](https://opensource.org/license/python-2-0)

### Python Libraries Used
#### Python
- **tkinter** - used for GUI development (Standard Library in Python, governed by Python's PSF License).
- **sys** - for interacting with the Python runtime environment (Standard Library in Python, governed by Python's PSF License).
- **json** - for working with JSON data and state management (Standard Library in Python, governed by Python's PSF License).
#### MicroPython
- **machine** - used for controlling hardware components (e.g. GPIO, PWM) (Standard Library in MicroPython, governed by the MIT License).
- **sys** - gives access to system parameters and functions, like managing the MicroPython runtime environment (Standard Library in MicroPython, governed by the MIT License).
- **time** - for handling time-related functions (Standard Library in MicroPython, governed by the MIT License).
