# DeepFace Industrial Access Control

A robust Face Recognition application designed for industrial access control scenarios, built with **DeepFace**, **PySide6**, and **OpenCV**.

## Features

-   **Industrial Interface**: LabVIEW-inspired UI with "Flash" visual feedback and bold controls.
-   **User Management**:
    -   Register new users with photo capture.
    -   Store metadata in SQLite and images in standard filesystem structure.
    -   Edit or delete existing users.
-   **Real-time Inference**:
    -   Live face recognition using DeepFace.
    -   Multi-threaded architecture for responsive UI.
    -   "Exit on Detect" mode for automated access.
    -   Visual feedback with Bounding Boxes and IDs.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd deepface-tests
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Launcher
Run the main entry point to open the Launcher:
```bash
python main.py
```

### Modes

1.  **Management (Gerenciamento)**:
    -   Add new users by capturing a photo from the webcam.
    -   Manage existing users (Search, Edit, Delete).

2.  **Recognition (Inferencia)**:
    -   Starts the camera and loads AI models.
    -   Displays bounding boxes for recognized users.

### CLI Arguments

-   `--exit-on-detect`: Automatically closes the application as soon as a known user is identified.
    ```bash
    python main.py --exit-on-detect
    ```

## Project Structure

-   `src/common`: Shared utilities (Database, Styles, Camera).
-   `src/features/cadastro`: Registration feature logic and UI.
-   `src/features/inferencia`: Recognition engine and UI.
