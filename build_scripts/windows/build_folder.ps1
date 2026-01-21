$ErrorActionPreference = "Stop"
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist\DeepFaceRec_Unified") { Remove-Item -Recurse -Force "dist\DeepFaceRec_Unified" }
if (Test-Path "DeepFaceRec_Unified.spec") { Remove-Item -Force "DeepFaceRec_Unified.spec" }


.\venv\Scripts\pyinstaller --noconfirm --onedir --noconsole --icon "$PWD\src\public\icons\certi-icon.ico" --name "DeepFaceRec_Unified" `
    --specpath "build" `
    --add-data "$PWD\src;src" `
    --add-data "$env:USERPROFILE\.deepface\weights;.deepface\weights" `
    --hidden-import "deepface" `
    --hidden-import "tensorflow" `
    --hidden-import "keras" `
    --hidden-import "h5py" `
    --collect-all "deepface" `
    --collect-all "tensorflow" `
    --collect-all "mtcnn" `
    --collect-all "keras" `
    --collect-all "h5py" `
    --collect-all "nicegui" `
    --collect-all "numpy" `
    --collect-all "pandas" `
    --collect-all "cv2" `
    --collect-all "scipy" `
    --collect-all "PIL" `
    --collect-all "webview" `
    "entry_point.py"

Write-Host "Folder build complete. Application is at dist/DeepFaceRec_Unified/DeepFaceRec_Unified.exe"
