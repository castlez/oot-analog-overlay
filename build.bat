@echo off
echo clearing build dirs if present
rmdir /S /Q "build"
rmdir /S /Q "dist"

echo installing pyinstaller
python -m pip install pyinstaller

echo building app
pyinstaller --onefile -w .\analog_disp.py --icon .\ess.ico
echo DONE safe to exit (hopefully)
pause