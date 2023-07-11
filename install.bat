@echo off
cls
echo 0. pywin32
echo 1. pyautogui
set /p m=Select(0)^>
cls
echo Installing keyboard ... (1/3)
pip install keyboard
cls
echo Installing Pillow ... (2/3)
pip install Pillow
cls
if %m%==1 (
echo Installing pyautogui ... (3/3)
pip install pyautogui
) ELSE (
echo Installing pywin32 ... (3/3)
pip install pywin32
)
cls
echo Installed:
echo - Keyboard
echo - Pillow
if %m%==1 (
echo - pyautogui
) ELSE (
echo - pywin32
)
pause