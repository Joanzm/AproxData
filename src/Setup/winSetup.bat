:: Building this applcation for windows system ...
@echo off
cd ..
del /s /q build\win32
python setup.py build
cd build\win32
FOR /F "USEBACKQ" %%F IN (`powershell -NoLogo -NoProfile -Command ^(Get-Item "AproxData\\AproxData.exe"^).VersionInfo.FileVersion`) DO (SET version=%%F)
7z a -tzip -y AproxData_v%version%.zip -o/AproxDatav%version% AproxData\*