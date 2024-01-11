# dynaMix: Applied Machine Learning Lab (2023-24)
_Basheq Tarifi, Laurie Johnston, Mauro Marino_
## Emotify: Mood-sensing for music recommendations

### Development Stack
- Instead of using the standard Arduino IDE, PlatformIO is used. This works in VS Code and provides a package library and much better project management and tools.
  - You can install it [here](https://platformio.org/install/ide?install=vscode) or just search PlatformIO in VS Code extensions.
- C/C++ is used for the actual code loaded to the Arduino.
- For the data collection, a Python script is used in conjunction with the Arduino code. A Pipenv is provided to maintain dependencies and versions (but not necessary if you install all the dependencies on your own Python):
  - Run `$ pip install --user pipenv` to install pipenv on your machine

### Getting started
In the root folder, run the following command to install all the Arduino dependencies:
```
pio pkg install
```
Run the following command to install the Python dependencies (and create the virtualenv if it does not exist):
```
pipenv install
```
