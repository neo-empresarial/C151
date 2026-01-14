
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

echo "Build complete. Executable is at dist/DeepFaceRec/DeepFaceRec"
