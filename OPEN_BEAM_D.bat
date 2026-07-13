@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title beam_d Launcher

 echo ============================================================
 echo   beam_d - Structural Beam Engineering Program
 echo ============================================================
 echo.

set "PYTHON_CMD="
where py >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    where python >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo [ERROR] Python was not found on this computer.
    echo.
    echo Install Python 3.10 or newer and select:
    echo   Add Python to PATH
    echo during installation.
    echo.
    start "" "https://www.python.org/downloads/windows/"
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] beam_d requires Python 3.10 or newer.
    echo.
    start "" "https://www.python.org/downloads/windows/"
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating the private beam_d Python environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :failure
) else (
    echo [1/3] Existing beam_d environment found.
)

set "VENV_PY=%CD%\.venv\Scripts\python.exe"

echo [2/3] Checking and installing required packages...
"%VENV_PY%" -m pip install --disable-pip-version-check --quiet --upgrade pip
if errorlevel 1 goto :failure

"%VENV_PY%" -m pip install --disable-pip-version-check --quiet -r requirements-app.txt -e .
if errorlevel 1 goto :failure

echo [3/3] Opening beam_d in your web browser...
echo.
echo Keep this window open while using the program.
echo Close this window to stop beam_d.
echo.

"%VENV_PY%" -m streamlit run app.py --server.headless false --browser.gatherUsageStats false
if errorlevel 1 goto :failure

exit /b 0

:failure
echo.
echo [ERROR] beam_d could not start.
echo Check your internet connection and the error message above.
echo.
pause
exit /b 1
