$ErrorActionPreference = "Stop"
$TargetFile = "$PSScriptRoot\..\..\dist\DeepFaceRec_Unified\DeepFaceRec_Unified.exe"
$ShortcutFile = "$Home\Desktop\Biometria.lnk"
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutFile)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = "$PSScriptRoot\..\..\dist\DeepFaceRec_Unified"
$Shortcut.IconLocation = "$TargetFile,0"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutFile"
