pyinstaller -F -y -w -n RetrocraftLauncher ./src/launcher.py
pyinstaller -F -y -w --add-data dist/RetrocraftLauncher:. -n RetrocraftInstaller ./src/installer.py
