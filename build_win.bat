pyinstaller -F -y -w --hidden-import winreg --uac-admin -n RetrocraftLauncher ./src/launcher.py
pyinstaller -F -y -w --hidden-import winreg --uac-admin --add-data dist/RetrocraftLauncher.exe;. -n RetrocraftInstaller ./src/installer.py
pause
