@echo off

REM Define Variables
set FILEPATH=C:\Users\magnus\Documents\Python\alinea_bot
set DESTINATION=\\192.168.1.13\Documents\alinea_bot

REM Copy Python script to SMB share and overwrite if it exists
echo Copying Python script to SMB share...
xcopy "%FILEPATH%\alinea.py" "%DESTINATION%" /Y /I
if %ERRORLEVEL% neq 0 (
    echo Failed to copy alinea.py to the SMB share. Exiting...
    exit /b 1
)

xcopy "%FILEPATH%\meow.env" "%DESTINATION%" /Y /I
if %ERRORLEVEL% neq 0 (
    echo Failed to copy meow.env to the SMB share. Exiting...
    exit /b 1
)

xcopy "%FILEPATH%\iceland_facts.py" "%DESTINATION%" /Y /I
if %ERRORLEVEL% neq 0 (
    echo Failed to copy iceland_facts.py to the SMB share. Exiting...
    exit /b 1
)

REM skibidi
echo SSH into server.net
ssh -t magnus@192.168.1.13 "sudo systemctl restart alinea_py" 

timeout /t 1.5