#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

rm -rf build_service dist/DeepFaceService *.spec

./venv/bin/pyinstaller --noconfirm --onefile --noconsole --name "DeepFaceService" \
    --specpath "build" \
    --exclude-module "nvidia" \
    --exclude-module "tensorrt" \
    --add-data "$(pwd)/src:src" \
    --hidden-import "deepface" \
    --hidden-import "encodings" \
    --hidden-import "tensorflow" \
    --hidden-import "tf_keras" \
    --hidden-import "PIL" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --hidden-import "pystray" \
    --hidden-import "cairo" \
    --collect-all "pystray" \
    --collect-all "cv2" \
    --collect-all "nicegui" \
    --collect-all "webview" \
    background_service.py

echo "Build complete. Executable is at dist/DeepFaceService"
