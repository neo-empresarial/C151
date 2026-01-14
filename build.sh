

# Backup existing database in dist if it exists
if [ -f "dist/DeepFaceRec/users.db" ]; then
    echo "Backing up existing users.db from dist..."
    cp dist/DeepFaceRec/users.db users.db.backup
fi

rm -rf build dist *.spec

./venv/bin/pyinstaller --noconfirm --onedir --windowed --name "DeepFaceRec" \
    --add-data "users.db:." \
    --add-data "src:src" \
    --hidden-import "deepface" \
    --hidden-import "tensorflow" \
    --hidden-import "tf_keras" \
    --hidden-import "cv2" \
    --hidden-import "PIL" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --collect-all "deepface" \
    --collect-all "tensorflow" \
    --collect-all "cv2" \
    main.py

# Restore database if backup exists
if [ -f "users.db.backup" ]; then
    echo "Restoring users.db to dist..."
    mv users.db.backup dist/DeepFaceRec/users.db
fi

echo "Build complete. Executable is at dist/DeepFaceRec/DeepFaceRec"
