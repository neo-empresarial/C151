[Setup]
AppName=FaceRecon
AppVersion=1.0
DefaultDirName={autopf}\FaceRecon
DefaultGroupName=FaceRecon
UninstallDisplayIcon={app}\FaceRecon-V0.exe
Compression=lzma2
SolidCompression=yes
OutputDir={#ProjectRoot}\dist
OutputBaseFilename=FaceRecon_Setup
SetupIconFile={#ProjectRoot}\src\public\icons\certi-icon.ico

[Files]
Source: "{#ProjectRoot}\dist\FaceRecon-V0\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FaceRecon"; Filename: "{app}\FaceRecon-V0.exe"; IconFilename: "{app}\_internal\src\public\icons\certi-icon.ico"
Name: "{autodesktop}\FaceRecon"; Filename: "{app}\FaceRecon-V0.exe"; IconFilename: "{app}\_internal\src\public\icons\certi-icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\FaceRecon-V0.exe"; Description: "{cm:LaunchProgram,FaceRecon}"; Flags: nowait postinstall skipifsilent
