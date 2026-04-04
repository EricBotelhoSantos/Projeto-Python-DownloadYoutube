[Setup]
; NexusTube Downloader — Inno Setup Configuration
AppName=NexusTubeDownloader
AppVersion=2.0
AppPublisher=Eric Botelho Santos
DefaultDirName={pf}\NexusTubeDownloader
DefaultGroupName=NexusTubeDownloader
; Output directory (relative to project root)
OutputDir=..\Instalador_Final
OutputBaseFilename=Instalar_NexusTubeDownloader_v2
; Wizard icon
SetupIconFile=..\desktop\assets\app_icon.ico
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos Adicionais:"

[Files]
; Main executable
Source: "..\dist\NexusTubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\NexusTubeDownloader"; Filename: "{app}\NexusTubeDownloader.exe"
; Desktop shortcut (optional)
Name: "{commondesktop}\NexusTubeDownloader"; Filename: "{app}\NexusTubeDownloader.exe"; Tasks: desktopicon

[Run]
; Launch after install
Filename: "{app}\NexusTubeDownloader.exe"; Description: "Iniciar NexusTubeDownloader agora"; Flags: nowait postinstall skipifsilent
