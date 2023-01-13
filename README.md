# Global variable based code generation tool for parametric Arduino projects
![lastupdate](https://img.shields.io/github/last-commit/joubiti/arduino-codegen)

## Overview
A simple Tkinter GUI developed with Python which aims to demonstrate a solution for non technical individuals to push updates to firmware reliant on 
global variables as parameters for its functions.


![image](https://user-images.githubusercontent.com/104909670/212356374-86badc0c-9725-4621-bd47-6f2c4cc46530.png)

A brief overview of what the app does:
- Given a parameter type and name, the code automatically generates new corresponding .ino sketch with the specified value
- Automatic main.cpp inclusion given the Arduino installation path folder in the options menu for makefile generation
- Forward prototype declarations for void (as of now) functions and automatic header inclusion for compilation purposes

## Usage
```
git clone https://github.com/joubiti/arduino-codegen
```

After connecting your Arduino board, you'll run the app:
```
python app.py
```
You'll get a user interface in which you'd have to first specify the path to your Arduino installation folder to automatically generate the makefile, as well as the path to your source .ino file that you wish to modify.
These parameters can be pre-defined in advance, you'll then select the COM port, the type and name of the variable with the desired value, and generate the code.

## To do
- Forward prototype declarations for any type of functions
- Integrate sudar's [makefile for Arduino](https://github.com/sudar/Arduino-Makefile) which will ensure high reliability as well as ability to automatically include any additional libraries on the source file for compilation
- an ESP32 based solution with integrated remote firmware updates.
