$ErrorActionPreference = "Stop"

if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }


.\venv\Scripts\pyinstaller --noconfirm --onefile --console --name "DeepFaceRec_Debug" `
    --add-data "users.db;." `
    --add-data "src;src" `
    --hidden-import "deepface" `
    --hidden-import "nicegui" `
    --hidden-import "scipy" `
    --hidden-import "webview" `
    --hidden-import "tensorflow" `
    --hidden-import "tf_keras" `
    --hidden-import "cv2" `
    --hidden-import "PIL" `
    --hidden-import "numpy" `
    --hidden-import "pandas" `
    --hidden-import "webview" `
    --collect-all "deepface" `
    --collect-all "tensorflow" `
    --collect-all "cv2" `
    main.py

Write-Host "Debug build complete. Executable is at dist/DeepFaceRec_Debug.exe"
