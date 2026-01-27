$ErrorActionPreference = "Stop"
$TargetFile = "$PSScriptRoot\FaceRecon-V0.exe"

if (-not (Test-Path $TargetFile)) {
    # Fallback for dev mode
    $TargetFile = "$PSScriptRoot\..\..\dist\FaceRecon-V0\FaceRecon-V0.exe"
}

$ShortcutFile = "$Home\Desktop\Biometria.lnk"
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutFile)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = Split-Path $TargetFile
$Shortcut.IconLocation = "$TargetFile,0"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutFile -> $TargetFile"
