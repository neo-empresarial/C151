# Core Modules (`src/core/`)

## Overview
This directory handles the "business logic" of the application, independent of the user interface.

## Files

### `database.py`
-   **Purpose**: Manages user data storage on the filesystem.
-   **Functionality**:
    -   Creates directories for new users.
    -   Saves user images.
    -   Deletes user data.
    -   Lists registered users.

### `recognition.py`
-   **Purpose**: Handles real-time face detection and recognition.
-   **Functionality**:
    -   Wraps the `DeepFace` library.
    -   Runs in a separate thread to prevent UI freezing.
    -   Processes video frames to find faces.
    -   Matches faces against the `database/` directory.
    -   Logs successful recognitions to `Logs/history.csv`.
