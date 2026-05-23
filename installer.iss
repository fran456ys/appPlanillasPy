[Setup]
AppName=Gestión de Terneros - Cabaña Pastoral
AppVersion=1.0
AppPublisher=Cabaña Pastoral
AppPublisherURL=
DefaultDirName={autopf}\appPlanillas
DefaultGroupName=Cabaña Pastoral
OutputDir=dist\installer
OutputBaseFilename=appPlanillas-setup
SetupIconFile=assets\fotoTernero.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Requiere Windows 10 o superior
MinVersion=10.0

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear ícono en el escritorio"; GroupDescription: "Íconos adicionales:"; Flags: checked

[Files]
Source: "dist\windows\appPlanillas.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Gestión de Terneros"; Filename: "{app}\appPlanillas.exe"
Name: "{commondesktop}\Gestión de Terneros"; Filename: "{app}\appPlanillas.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\appPlanillas.exe"; Description: "Abrir la aplicación"; Flags: nowait postinstall skipifsilent
