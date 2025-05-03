
[Setup]
AppName=Easy AI Keyword Tool
AppVersion=1.0
DefaultDirName={pf}\Easy AI Keyword Tool
DefaultGroupName=Easy AI Tools
OutputDir=.
OutputBaseFilename=EasyAI_Installer
SetupIconFile=easy_ai_icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Easy AI Keyword Tool.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Easy AI Keyword Tool"; Filename: "{app}\Easy AI Keyword Tool.exe"
Name: "{group}\Uninstall Easy AI Keyword Tool"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Easy AI Keyword Tool"; Filename: "{app}\Easy AI Keyword Tool.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
