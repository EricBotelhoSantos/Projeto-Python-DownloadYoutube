[Setup]
; Configurações Básicas do Instalador
AppName=NexusTubeDownloader
AppVersion=2.0
AppPublisher=Eric Botelho Santos
DefaultDirName={pf}\NexusTubeDownloader
DefaultGroupName=NexusTubeDownloader
; Onde o instalador final será gerado e qual o nome dele
OutputDir=.\Instalador_Final
OutputBaseFilename=Instalar_NexusTubeDownloader_v2
; Ícone do próprio "Wizard" de instalação
SetupIconFile=app_icon.ico
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos Adicionais:"

[Files]
; Copia o executável principal que criamos
Source: "dist\NexusTubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Cria atalho no Menu Iniciar
Name: "{group}\NexusTubeDownloader"; Filename: "{app}\NexusTubeDownloader.exe"
; Cria atalho na Área de Trabalho caso o usuário marque a caixinha
Name: "{commondesktop}\NexusTubeDownloader"; Filename: "{app}\NexusTubeDownloader.exe"; Tasks: desktopicon

[Run]
; Oferece opção de abrir o App assim que o instalador termina
Filename: "{app}\NexusTubeDownloader.exe"; Description: "Iniciar NexusTubeDownloader agora"; Flags: nowait postinstall skipifsilent
