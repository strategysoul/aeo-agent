@echo off
rem Runs the AEO agent unattended for every site under AEO_ROOT. Usage: run-aeo.cmd daily^|weekly
rem Written by /aeo-agent:aeo setup. Edit ALLOWED if you add or remove connectors.
setlocal
set "MODE=%~1"
if "%MODE%"=="" set "MODE=weekly"
if "%AEO_ROOT%"=="" (set "ROOT=%USERPROFILE%\Documents\AEO") else (set "ROOT=%AEO_ROOT%")
set "ALLOWED=__ALLOWED_TOOLS__"
if not exist "%ROOT%\logs" mkdir "%ROOT%\logs"
cd /d "%ROOT%"
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "TODAY=%%d"
claude -p "/aeo-agent:aeo --all %MODE% --scheduled" --permission-mode acceptEdits --allowedTools "%ALLOWED%" >> "%ROOT%\logs\%MODE%-%TODAY%.log" 2>&1
