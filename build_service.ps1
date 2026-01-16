$ErrorActionPreference = "Stop"

if (Test-Path "dist/DeepFaceService.exe") { Remove-Item -Force "dist/DeepFaceService.exe" }

Write-Host "Building DeepFaceService (Hidden Camera Service)..."

.\venv\Scripts\pyinstaller DeepFaceService.spec --noconfirm --clean

Write-Host "Build complete. Executable should be at dist/DeepFaceService.exe"
