$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..\..

$processName = "FaceRecon-V0"
$processes = Get-Process $processName -ErrorAction SilentlyContinue
if ($processes) {
    Write-Host "Killing running instances of $processName..."
    $processes | Stop-Process -Force
    Start-Sleep -Seconds 2
}

if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist/FaceRecon-V0") { Remove-Item -Recurse -Force "dist/FaceRecon-V0" }
if (Test-Path "FaceRecon-V0.spec") { Remove-Item -Force "FaceRecon-V0.spec" }


.\venv\Scripts\pyinstaller --noconfirm --onedir --icon "$PWD\src\public\icons\certi-icon.ico" --name "FaceRecon-V0" `
    --splash "$PWD\src\public\images\certi\splash-screen.png" `
    --specpath "build" `
    --add-data "$PWD\src;src" `
    --add-data "$env:USERPROFILE\.deepface\weights;.deepface\weights" `
    --add-binary "C:\Windows\System32\msvcp140_1.dll;." `
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

Write-Host "Build complete. Output folder is at dist/FaceRecon-V0"
Copy-Item "build_scripts\windows\create_shortcut.ps1" -Destination "dist\FaceRecon-V0\create_shortcut.ps1"
Write-Host "Shortcut script copied to dist/FaceRecon-V0"

$isccPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
$issFile = "build_scripts\windows\setup.iss"

if (Test-Path $isccPath) {
    if (Test-Path $issFile) {
        Write-Host "Inno Setup found. Compiling installer..."
        $ProjectRoot = $PWD.Path
        & $isccPath "/DProjectRoot=$ProjectRoot" $issFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Installer created successfully at dist/FaceRecon_Setup.exe" -ForegroundColor Green
        } else {
            Write-Host "Installer compilation failed." -ForegroundColor Red
        }
    } else {
        Write-Host "Setup script not found at $issFile" -ForegroundColor Yellow
    }
} else {
    Write-Host "Inno Setup Compiler (ISCC.exe) not found at default location." -ForegroundColor Yellow
    Write-Host "Please install Inno Setup to generate the installer setup.exe automatically."
    Write-Host "Download: https://jrsoftware.org/isdl.php"
}

