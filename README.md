# DeepFace Real-Time Recognition App

## Overview
A modular, cross-platform desktop application for real-time face recognition and user management. Built with **Python 3.12**, **PySide6 (Qt)**, and **DeepFace**.

## Project Structure
```
DeepFaceRec/
├── database/            # Stores user images (1 folder per user)
├── dist/                # Contains the compiled executable
├── Logs/                # Recognition history (CSV)
├── src/                 # Source code
│   ├── core/            # Backend logic (Database, Recognition)
│   └── gui/             # Frontend logic (PySide6 Windows)
├── main.py              # Application entry point
├── build.sh             # Linux build script (PyInstaller)
└── requirements.txt     # Python dependencies
```

## Application Flow

### 1. Initialization
-   The application starts via `main.py`.
-   It parses command-line arguments to determine the mode.
-   If no arguments are provided, the **Launcher Window** (`src/gui/main_window.py`) is shown.

### 2. Recognition Mode (`--mode recognition`)
-   Initializes the `RecognitionEngine` (`src/core/recognition.py`).
-   Loads the **FaceNet** model (downloaded to `~/.deepface` on first run).
-   Captures video from the default webcam.
-   Detects faces and compares embeddings against the `database/` folder.
-   Updates the UI (`src/gui/recognition_ui.py`) with bounding boxes (Green=Known, Red=Unknown).
-   Logs recognitions to `Logs/history.csv` (max once per minute per user).

### 3. Management Mode (`--mode manage`)
-   Opens the User Manager (`src/gui/management_ui.py`).
-   **Register**: Captures a frame from the webcam and saves it as `database/{Name}/{Name}.jpg`.
-   **Edit**: Allows updating the detection photo for an existing user.
-   **Delete**: Removes the user's folder and data.
-   Automatically clears internal caches (`.pkl` files) to ensure immediate recognition updates.

## Executable Usage
The application is compiled into a standalone binary in the `dist/` folder.

**Run Launcher:**
```bash
./dist/DeepFaceRec
```

**Run Specific Modes:**
```bash
./dist/DeepFaceRec --mode recognition
./dist/DeepFaceRec --mode manage
```

## Licenses
-   **DeepFace**: [MIT License](https://github.com/serengil/deepface/blob/master/LICENSE) - Copyright (c) 2020 Sefik Ilkin Serengil
-   **TensorFlow**: [Apache 2.0](https://github.com/tensorflow/tensorflow/blob/master/LICENSE)
-   **PySide6 (Qt)**: [LGPLv3](https://doc.qt.io/qtforpython-6/licenses.html)
-   **OpenCV**: [Apache 2.0](https://github.com/opencv/opencv/blob/4.x/LICENSE)

## Credits
Developed for educational and demonstration purposes showing the integration of Deep Learning with modern Desktop GUIs.
