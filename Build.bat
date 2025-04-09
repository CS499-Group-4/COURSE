@echo off
REM Activate the virtual environment
call .\build_venv\Scripts\activate.bat

REM Run PyInstaller to build the executable
pyinstaller --onefile ^
  --add-data "./icon;icon" ^
  --add-data "./pages;pages" ^
  --add-data "./lib;lib" ^
  --workpath "./build/temp" ^
  --distpath "./build" ^
  --noconsole ^
  course.py

REM Optional: pause to see any output/errors before the window closes
pause
