$envFilePath = ".\.env"

$content = Get-Content -Path $envFilePath

if (-Not $content) {
    Write-Output "Create a file with named '.env' (See README)"
    Exit
}

$RadonUlzerfilePathLine = $content | Where-Object { $_ -match '^RadonUlzer_PATH=' }

if ($RadonUlzerfilePathLine) {
    $RadonUlzerFilePath = $RadonUlzerfilePathLine -split '=' | Select-Object -Last 1
    Write-Output "Der Dateipfad ist: $RadonUlzerFilePath"
} else {
    Write-Output "Key RadonUlzer_PATH not found"
    Exit
}

$SpaceShipRadarfilePathLine = $content | Where-Object { $_ -match '^SpaceShipRadar_PATH=' }

if ($SpaceShipRadarfilePathLine) {
    $SpaceShipRadarFilePath = $SpaceShipRadarfilePathLine -split '=' | Select-Object -Last 1
    Write-Output "Der Dateipfad ist: $SpaceShipRadarFilePath"
} else {
    Write-Output "Key SpaceShipRadar_PATH not found"
    Exit
}

# activate venv
# .\venv\Scripts\activate

Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=Zumo0 --stdout-redirect $RadonUlzerFilePath;"
Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=Zumo1 --stdout-redirect $RadonUlzerFilePath;"
Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=Zumo2 --stdout-redirect $RadonUlzerFilePath;"
Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=Zumo4 --stdout-redirect $RadonUlzerFilePath;"
Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=Zumo5 --stdout-redirect $RadonUlzerFilePath;"

Start-Process powershell "& '${env:WEBOTS_HOME}\msys64\mingw64\bin\webots-controller.exe' --robot-name=MyBot --stdout-redirect $SpaceShipRadarFilePath;"
