#define MyAppName "JANET"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "JANET Bio AI"
#define MyAppExeName "JANET.exe"

[Setup]
AppId={{BB3E7873-7E6B-47D1-9B0E-C902BE7AB224}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\JANET
DefaultGroupName=JANET
AllowNoIcons=yes
OutputDir=..\installer-output
OutputBaseFilename=JANETSetup
SetupIconFile=..\assets\janet_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut for JANET"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\JANET\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\assets\janet_icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{group}\JANET"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\janet_icon.ico"
Name: "{autodesktop}\JANET"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\janet_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch JANET"; Flags: nowait postinstall skipifsilent
