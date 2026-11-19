
; Smart Download Organizer - Windows Installer
; Created using Inno Setup 7

#define MyAppName "Smart Download Organizer"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Aahish Aayan (Silver Bullet)"
#define MyAppExeName "SmartDownloadOrganizer.exe"

#define ProjectDir "A:\Nexus\Coding\Projects\intelligent-systems\automations\smart-download-organizer"
#define SourceDir ProjectDir + "\dist\SmartDownloadOrganizer"

[Setup]

; Application identity - preserve this GUID for future releases.
AppId={{AF13A4F5-76E8-42AD-A0E9-E28B7475922D}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

; Install for the current user without normally requiring admin rights.
DefaultDirName={autopf}\{#MyAppName}
PrivilegesRequired=lowest

; Supported Windows architecture.
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Installer appearance and output.
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
SetupIconFile={#ProjectDir}\assets\icons\app_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

LicenseFile={#ProjectDir}\LICENSE

OutputDir={#ProjectDir}\releases
OutputBaseFilename=SmartDownloadOrganizer-Setup

Compression=lzma
SolidCompression=yes
WizardStyle=modern dynamic

; Uninstaller and version information.
Uninstallable=yes
VersionInfoCompany={#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; \
    Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; \
    Flags: unchecked

[Files]
; Include the complete PyInstaller one-folder distribution.
Source: "{#SourceDir}\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu shortcut.
Name: "{autoprograms}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"

; Optional desktop shortcut.
Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
; Allow the user to launch the application after installation.
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#MyAppName}}"; \
    Flags: nowait postinstall skipifsilent
