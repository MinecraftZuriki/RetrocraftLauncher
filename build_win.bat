pyinstaller -F -y --hidden-import winreg -w --uac-admin ./src/installer.py
pyinstaller -F -y --hidden-import winreg -w --uac-admin ./src/launcher.py