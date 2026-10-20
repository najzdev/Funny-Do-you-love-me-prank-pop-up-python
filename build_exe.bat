@echo off
setlocal

python -m pip install --upgrade pyinstaller
python -m PyInstaller --clean --noconfirm meow.spec

echo.
echo Built executable: dist\DoYouLoveMe.exe
pause
