# Source Code (`src/`)

This directory contains the modularized source code for the application.

## Directory Structure

### `common/`
Shared utility modules used across the application:
-   `database.py`: Handles SQLite connection and file system operations for user data.
-   `styles.py`: Defines the Industrial/LabVIEW-style color palette and stylesheet.
-   `camera.py`: Manages OpenCV video capture in a thread-safe manner with Qt Signals.
-   `logger.py`: Centralized logging utility.

### `features/`
Feature-specific modules:

#### `cadastro/` (Registration)
-   `ui_cadastro.py`: The User Management window. Handles photo capture (freeze/flash), saving to database, and list management.

#### `inferencia/` (Inference)
-   `engine.py`: The `RecognitionWorker` that runs `DeepFace.find()` in a separate thread.
-   `ui_inferencia.py`: The Recognition window. Handles the Loading Overlay, video display, and visual results (Bounding Boxes).

## Development
To add a new feature:
1.  Create a new directory in `features/`.
2.  Implement your logic and UI.
3.  Expose the entry point (e.g., a Window class).
4.  Update `main.py` to route to your new feature.
