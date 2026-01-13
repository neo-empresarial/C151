#!/bin/bash

# Clean previous builds
rm -rf build dist *.spec

# Run PyInstaller
# --onefile: Create a single executable file
# --windowed: Do not show a console window (GUI mode)
# --name: Name of the executable
# --add-data: Include the database folder (On Linux use : as separator, Windows use ;)
# --hidden-import: Explicitly import hidden dependencies
# --collect-all: Collect all data for deepface to ensure internal config files are present

./venv/bin/pyinstaller --noconfirm --onefile --windowed --name "DeepFaceRec" \
    --add-data "database:database" \
    --add-data "src:src" \
    --hidden-import "deepface" \
    --hidden-import "tensorflow" \
    --hidden-import "tf_keras" \
    --hidden-import "cv2" \
    --hidden-import "PIL" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --hidden-import "PySide6" \
    --hidden-import "src.gui.main_window" \
    --hidden-import "src.gui.recognition_ui" \
    --hidden-import "src.gui.management_ui" \
    --hidden-import "src.gui.styles" \
    --hidden-import "src.core.database" \
    --hidden-import "src.core.recognition" \
    --collect-all "deepface" \
    --collect-all "tensorflow" \
    --collect-all "PySide6" \
    main.py

echo "Build complete. Executable is in dist/DeepFaceRec"
