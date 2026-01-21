$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..\..

if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist/DeepFaceRec_Unified.exe") { Remove-Item -Force "dist/DeepFaceRec_Unified.exe" }
if (Test-Path "DeepFaceRec_Unified.spec") { Remove-Item -Force "DeepFaceRec_Unified.spec" }


.\venv\Scripts\pyinstaller --noconfirm --onefile --console --name "DeepFaceRec_Unified" `
    --specpath "build" `
    --splash "$PWD\src\public\images\certi\logo-certi.png" `
    --add-data "$PWD\src;src" `
    --add-data "$env:USERPROFILE\.deepface\weights;.deepface\weights" `
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
    --hidden-import "faiss" `
    --hidden-import "torch" `
    --hidden-import "torchvision" `
    --collect-all "faiss" `
    --collect-all "deepface" `
    --collect-all "tensorflow" `
    --collect-all "cv2" `
    --collect-all "nicegui" `
    --collect-all "webview" `
    --collect-all "mtcnn" `
    entry_point.py

Write-Host "Unified build complete. Executable is at dist/DeepFaceRec_Unified.exe"
