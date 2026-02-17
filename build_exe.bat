@echo off
echo Building Grae-X Magic Eye Shield...
echo.

echo Option 1: Nuitka (recommended)
echo.
python -m nuitka --onefile --windows-disable-console --windows-icon-from-ico=icon.ico --output-dir=dist src/main.py
echo.

echo Option 2: PyInstaller
echo.
python -m PyInstaller --onefile --windowed --name "Grae-X Magic Eye Shield" --icon=icon.ico src/main.py
echo.

echo Build complete! Check the 'dist' folder.
pause