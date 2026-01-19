$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..\..

if (Test-Path "dist/DeepFaceService.exe") { Remove-Item -Force "dist/DeepFaceService.exe" }

Write-Host "Building DeepFaceService (Hidden Camera Service)..."

.\venv\Scripts\pyinstaller --noconfirm --onefile --noconsole --name "DeepFaceService" `
    --specpath "build" `
    --exclude-module "nvidia" `
    --exclude-module "tensorrt" `
    --add-data "$PWD\src;src" `
    --hidden-import "deepface" `
    --hidden-import "encodings" `
    --hidden-import "tensorflow" `
    --hidden-import "tf_keras" `
    --hidden-import "PIL" `
    --hidden-import "numpy" `
    --hidden-import "pandas" `
    --hidden-import "pystray" `
    --hidden-import "cairo" `
    --collect-all "pystray" `
    --collect-all "cv2" `
    --collect-all "nicegui" `
    --collect-all "webview" `
    background_service.py

Write-Host "Build complete. Executable should be at dist/DeepFaceService.exe"
