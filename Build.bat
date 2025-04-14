@echo off

REM Use python (not python3) on Windows

echo ------------------------------------------------
echo Creating virtual environment...
echo ------------------------------------------------
python -m venv build_venv


echo ------------------------------------------------
echo Activating virtual environment
echo ------------------------------------------------
call build_venv\Scripts\activate.bat

echo ----------------------------------------------
echo Upgrading pip...
echo ----------------------------------------------
python -m pip install --upgrade pip

@REM echo Pre-Checking packages...
@REM pip freeze

REM Check if requirements have been installed before using a marker file
if not exist build_venv\requirements_installed.flag (
    echo ------------------------------------------------
    echo Installing required packages...
    echo ------------------------------------------------
    if exist "venv_requirements.txt" (
        python -m pip install -r venv_requirements.txt
        if errorlevel 1 (
            echo ------------------------------------------------
            echo Failed to install required packages.
            echo ------------------------------------------------
            pause
            exit /b 1
        )
        REM Create a marker file to signal that installation was done
        echo ------------------------------------------------
        echo installed > build_venv\requirements_installed.flag
        echo ------------------------------------------------
    ) else (
        echo ------------------------------------------------
        echo venv_requirements.txt not found.
        echo ------------------------------------------------
        pause
        exit /b 1
    )
) else (
    echo ---------------------------------------------------
    echo Required packages already installed.
    echo ---------------------------------------------------
)

@REM echo Post-Checking packages...
@REM pip freeze

REM Delete previous build folder if it exists
if exist "build" (
    echo ------------------------------------------------
    echo Deleting existing build folder...
    echo ------------------------------------------------
    rmdir /s /q build
)

echo ------------------------------------------------
echo Building with PyInstaller...
echo ------------------------------------------------
timeout /t 2 /nobreak >nul
python -m PyInstaller --onefile ^
  --add-data "./icon;icon" ^
  --add-data "./pages;pages" ^
  --add-data "./lib;lib" ^
  --workpath "./build/temp" ^
  --distpath "./build" ^
  --noconsole ^
  course.py

pause