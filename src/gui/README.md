# GUI Modules (`src/gui/`)

## Overview
This directory contains all the visual components of the application, built using the **PySide6** (Qt) framework.

## Files

### `main_window.py`
-   **Class**: `LauncherWindow`
-   **Purpose**: The entry point window that allows the user to choose between Recognition and Management modes.

### `recognition_ui.py`
-   **Class**: `RecognitionWindow`
-   **Purpose**: Displays the webcam feed with real-time overlays.
-   **Flow**:
    1.  Starts the `RecognitionEngine`.
    2.  Captures video frames.
    3.  Draws green/red boxes based on engine results.

### `management_ui.py`
-   **Class**: `ManagementWindow`
-   **Purpose**: A CRUD (Create, Read, Update, Delete) interface for user management.
-   **Features**:
    -   List registered users.
    -   Add new users via webcam.
    -   Update existing user photos.
    -   Delete users.

### `styles.py`
-   **Purpose**: Defines the VSCode-inspired dark theme (colors, fonts, stylesheet strings) used by all windows.
