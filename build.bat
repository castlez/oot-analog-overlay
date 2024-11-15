@echo off
echo clearing build dirs if present
rmdir /S /Q ".\build"
rmdir /S /Q ".\dist"
rmdir /S /Q ".\ess_overlay_windows"

echo installing pyinstaller
python -m pip install pyinstaller

echo building app
pyinstaller --onefile -w .\analog_disp.py --icon .\ess.ico

echo copy over readme and sample config to dist
xcopy .\README.md .\dist\
xcopy .\config.txt .\dist

echo renaming dist to ess_overlay_windows
rename dist ess_overlay_windows

echo DONE safe to exit (hopefully)
pause