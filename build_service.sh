#!/bin/bash
set -e

rm -rf build_service dist/DeepFaceService *.spec

./venv/bin/pyinstaller --noconfirm --onedir --windowed --name "DeepFaceService" \
    --exclude-module "nvidia" \
    --exclude-module "tensorrt" \
    --add-data "users.db:." \
    --add-data "src:src" \
    --hidden-import "deepface" \
    --hidden-import "encodings" \
    --hidden-import "tensorflow" \
    --hidden-import "tf_keras" \
    --hidden-import "PIL" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --hidden-import "pystray" \
    --hidden-import "cairo" \
    --collect-all "deepface" \
    --collect-all "pystray" \
    --collect-all "cv2" \
    src/background_service.py

echo "Build complete. Executable is at dist/DeepFaceService"
