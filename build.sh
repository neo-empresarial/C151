#!/bin/bash
set -e

if [ -f "dist/DeepFaceRec/users.db" ]; then
    echo "Backing up existing users.db from dist..."
    cp dist/DeepFaceRec/users.db users.db.backup
elif [ -f "dist/users.db" ]; then
    cp dist/users.db users.db.backup
fi

rm -rf build dist *.spec

./venv/bin/pyinstaller --noconfirm --onefile --windowed --name "DeepFaceRec" \
    --splash "src/public/images/certi/logo-certi.png" \
    --add-data "users.db:." \
    --add-data "src:src" \
    --hidden-import "deepface" \
    --hidden-import "tensorflow" \
    --hidden-import "tf_keras" \
    --hidden-import "cv2" \
    --hidden-import "PIL" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --hidden-import "webview" \
    --collect-all "deepface" \
    --collect-all "tensorflow" \
    --collect-all "cv2" \
    main.py

if [ -f "users.db.backup" ]; then
    echo "Restoring users.db to dist..."
    if [ ! -d "dist" ]; then mkdir dist; fi
    mv users.db.backup dist/users.db
fi

echo "Build complete. Executable is at dist/DeepFaceRec"
