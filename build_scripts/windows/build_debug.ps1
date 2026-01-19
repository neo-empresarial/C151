$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..\..

if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "DeepFaceRec_Debug.spec") { Remove-Item -Force "DeepFaceRec_Debug.spec" }


.\venv\Scripts\pyinstaller --noconfirm --onefile --console --name "DeepFaceRec_Debug" `
    --specpath "build" `
    --add-data "$PWD\users.db;." `
    --add-data "$PWD\src;src" `
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
    --hidden-import "pandas" `
    --hidden-import "webview" `
    --hidden-import "faiss" `
    --collect-all "faiss" `
    --collect-all "deepface" `
    --collect-all "tensorflow" `
    --collect-all "cv2" `
    --collect-all "nicegui" `
    --collect-all "webview" `
    --collect-all "mtcnn" `
    main.py

Write-Host "Debug build complete. Executable is at dist/DeepFaceRec_Debug.exe"
