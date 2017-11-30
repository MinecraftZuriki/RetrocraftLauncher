#!/usr/bin/env python3

import sys
import os
import shutil
import platform
import time
import distutils
import subprocess
#import PyQt5
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets

isWindows = False
isLinux = False
isMac = False
if(platform.system() == "Windows"):
    isWindows = True
elif(platform.system() == "Mac"):
    isMac = True
else:
    isLinux = True
#end if

if(isWindows):
    import winreg
#end if

class Config:
    __installPath = None
    __multiMcPath = None

    @staticmethod
    def exists():
        return os.path.exists(Config.settingsLocation())
    #end def

    @staticmethod
    def load():
        if(Config.exists()):
            f = open(Config.settingsLocation(), "r")
            data = f.readlines()
            f.close()
            for l in data:
                pair = l.split("=")
                if(pair[0]=="InstallPath"):
                    Config.__installPath = pair[1]
                elif(pair[0]=="MultiMcPath"):
                    Config.__multiMcPath = pair[1]
                #end if
        else:
            raise FileNotFoundError()
        #end def
    #end def

    @staticmethod
    def save():
        if(not Config.exists()):
            # create all folders to designated settings location minus settings file itself
            os.makedirs(os.path.abspath(os.path.join(Config.settingsLocation(), os.path.pardir)), exist_ok=True)
        #end if
        f = open(Config.settingsLocation(), "w+") # open for writing, create if not exists
        lines = ["InstallPath="+Config.__installPath, "MultiMcPath="+Config.__multiMcPath]
        f.write("\n".join(lines))
        f.flush()
        f.close()
    #end def

    @staticmethod
    def installPath(value=None):
        if(value==None):
            if(Config.__installPath==None):
                Config.load()
            #end if
            return Config.__installPath
        else:
            Config.__installPath = value
        #end if
    #end def

    @staticmethod
    def multiMcPath(value=None):
        if(value==None):
            if(Config.__multiMcPath==None):
                Config.load()
            #end if
            return Config.__multiMcPath
        else:
            Config.__multiMcPath = value
        #end if
    #end def

    @staticmethod
    def settingsLocation():
        if(isWindows):
            return os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "retrocraft", "launcher", "settings.dat")
        elif(isMac):
            return os.path.join(os.path.expanduser("~"), "Library", "Preferences", "retrocraft", "launcher", "settings.dat")
        elif(isLinux):
            return os.path.join(os.path.expanduser("~"), ".config", "retrocraft", "launcher", "settings.dat")
        else:
            raise Exception("Unknown OS version")
        #end if
    #end def
#end class

class MainWindow(QtWidgets.QWidget):

    fioInstallPath = None
    tbInstallPath = None
    tbMultiMCPath = None

    tbLogWindow = None

    def __init__(self):
        super().__init__()
        self.init_ui()
    #end def

    def init_ui(self):
        self.setWindowTitle("Install Retrocraft Classic Launcher")
        self.setFixedSize(480, 320)

        self.fioInstallPath = QtWidgets.QFileDialog()
        self.tbLogWindow = QtWidgets.QTextBrowser()

        self.tbLogWindow.setFont(Qt.QFont("Courier New"))

        vbox = QtWidgets.QVBoxLayout()

        lbTitle = QtWidgets.QLabel()
        lbTitle.setText("Install Retrocraft Classic Launcher")
        lbTitle.setFont(Qt.QFont("Microsoft Sans Serif", 16))
        lbTitle.setMargin(10)

        # Install Path Tool
        hboxInstallPath = QtWidgets.QHBoxLayout()

        lbInstallPath = QtWidgets.QLabel()
        lbInstallPath.setText("Install Path:")
        lbInstallPath.setMinimumWidth(80)
        lbInstallPath.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.tbInstallPath = QtWidgets.QLineEdit()

        btnInstallPath = QtWidgets.QPushButton()
        btnInstallPath.setText("Browse")
        btnInstallPath.clicked.connect(self.selectInstallPath)

        hboxInstallPath.addWidget(lbInstallPath)
        hboxInstallPath.addWidget(self.tbInstallPath)
        hboxInstallPath.addWidget(btnInstallPath)

        # MultiMC Path Tool
        hboxMultiMCPath = QtWidgets.QHBoxLayout()

        lbMultiMCPath = QtWidgets.QLabel()
        lbMultiMCPath.setText("MultiMC Path:")
        lbMultiMCPath.setMinimumWidth(80)
        lbMultiMCPath.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.tbMultiMCPath = QtWidgets.QLineEdit()

        btnMultiMCPath = QtWidgets.QPushButton()
        btnMultiMCPath.setText("Browse")
        btnMultiMCPath.clicked.connect(self.selectMultiMCPath)

        hboxMultiMCPath.addWidget(lbMultiMCPath)
        hboxMultiMCPath.addWidget(self.tbMultiMCPath)
        hboxMultiMCPath.addWidget(btnMultiMCPath)

        hboxInteractions = QtWidgets.QHBoxLayout()

        btnInstall = QtWidgets.QPushButton()
        btnInstall.setText("Install")

        btnCancel = QtWidgets.QPushButton()
        btnCancel.setText("Cancel")
        btnCancel.clicked.connect(sys.exit)

        btnInstall.clicked.connect(btnCancel.setDisabled)
        btnInstall.clicked.connect(install)

        hboxInteractions.addStretch()
        hboxInteractions.addWidget(btnInstall)
        hboxInteractions.addWidget(btnCancel)

        vbox.addWidget(lbTitle)
        vbox.addLayout(hboxInstallPath)
        vbox.addLayout(hboxMultiMCPath)
        vbox.addWidget(self.tbLogWindow)
        vbox.addLayout(hboxInteractions)
        vbox.addStretch()

        self.setLayout(vbox)
        self.show()
    #end def

    def logMessage(self, message, level=0):
        if(level == 1):
            self.tbLogWindow.append("<span style='color:red'>" + message + "</span>")
        else:
            self.tbLogWindow.append("<span>" + message + "</span>")
        #end if
    #end def

    def selectInstallPath(self):
        if (self.tbInstallPath.text()!=""):
            self.fioInstallPath.setDirectory(os.path.abspath(os.path.join(self.tbInstallPath.text(), "..")))
            #except: pass
        #end if
        self.fioInstallPath.setFileMode(4)
        self.fioInstallPath.setWindowModality(QtCore.Qt.ApplicationModal)
        # Blocks main thread execution
        if(self.fioInstallPath.exec_()==1):
            # Seems like a really shitty way to do this
            self.tbInstallPath.setText(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], "RetrocraftLauncher")))
        #end if
    #end def

    def selectMultiMCPath(self):
        if (self.tbMultiMCPath.text()!=""):
            self.fioInstallPath.setDirectory(os.path.abspath(os.path.join(self.tbMultiMCPath.text(), "..")))
            #except: pass
        #end if
        self.fioInstallPath.setFileMode(4)
        self.fioInstallPath.setWindowModality(QtCore.Qt.ApplicationModal)
        # Blocks main thread execution
        if(self.fioInstallPath.exec_()==1):
            exe = None
            if(isWindows):
                exe = "MultiMC.exe"
            elif(isMac):
                exe = "MultiMC.app"
            elif(isLinux):
                exe = "MultiMC"
            else:
                infoDialog("Unknown OS, can't check if directory is valid.\n\nProceed at your own risk.")
                self.tbMultiMCPath.setText(os.path.abspath(self.fioInstallPath.selectedFiles()[0]))
            if(os.path.exists(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], exe))) and os.path.isfile(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], exe)))):
                # Seems like a really shitty way to do this5
                self.tbMultiMCPath.setText(os.path.abspath(self.fioInstallPath.selectedFiles()[0]))
            else:
                errorDialog("Unable to find MultiMC executable.\n\nSelect the base MultiMC directory containing,\nthe MultiMC executable file.")
            #end if
        #end if
    #end def
#end class

def errorDialog(message):
    dlg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error", message, QtWidgets.QMessageBox.Ok)
    return dlg.exec_()
#end def

def warningDialog(message):
    dlg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Warning", message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    return dlg.exec_()
#end def

def infoDialog(message):
    dlg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Info", message, QtWidgets.QMessageBox.Ok)
    return dlg.exec_()
#end def

def install(self):
    window.logMessage("Beginning installation...")
    overwrite = True
    if(Config.exists()):
        window.logMessage("Detected existing installation!")
        dialog = warningDialog("A previous installation of Retrocraft Launcher was detected.\n\nOverwrite?")
        if(dialog == QtWidgets.QMessageBox.Yes):
            window.logMessage("User initiated overwrite")
            overwrite = True
        else:
            window.logMessage("User initiated abort!")
            overwrite = False
        #end if
    if(overwrite):
        # Pre-Install checks

        if(os.path.abspath(window.tbInstallPath.text()) != window.tbInstallPath.text()):
            window.logMessage("Path in unexpected format, aborting installation!", 1)
            errorDialog("Path in unexpected format, aborting installation!")
            return
        #end if
        Config.installPath(window.tbInstallPath.text())
        if(os.path.abspath(window.tbInstallPath.text()) != window.tbInstallPath.text()):
            window.logMessage("Path in unexpected format, aborting installation!", 1)
            errorDialog("Path in unexpected format, aborting installation!")
            return
        #end if
        exe = None
        if(isWindows):
            exe = "MultiMC.exe"
        elif(isMac):
            exe = "MultiMC.app"
        elif(isLinux):
            exe = "MultiMC"
        else:
            window.logMessage("Unknown OS, can't check if directory is valid.", 1)
            dialog = warnDialog("Unknown OS, can't check if directory is valid.\n\nProceed at your own risk.")
            if(dialog == QtWidgets.QMessageBox.No):
                window.logMessage("User aborted installation!", 1)
                infoDialog("Installation cancelled.")
                return
            #end if
        #end if
        if(exe == None):
            print("")
        else:
            if(not os.path.exists(os.path.abspath(os.path.join(window.tbMultiMCPath.text(), exe))) or not os.path.isfile(os.path.abspath(os.path.join(window.tbMultiMCPath.text(), exe)))):
                # Redundant check for MultiMC.exe just in case someone manipulates the path manually...
                window.logMessage("Unable to find MultiMC installation, selected directory may be incorrect.", 1)
                errorDialog("Path in unexpected format, aborting installation!")
                return
            #end if
        #end if
        Config.multiMcPath(window.tbMultiMCPath.text())

        try:
            # Save configuration file
            window.logMessage("Writing config...")
            Config.save()
        except:
            errorDialog("Unable to write config!\n\nAborting installation.")
            window.logMessage("Unable to write config, aborting installation!", 1)
            return
        #end try

        # Install Protocol Handler
        if(isWindows):
            try:
                window.logMessage("Creating protocol handler registry keys...")
                regMainKey = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, "Software\\Classes\\retrocraft", 0, winreg.KEY_ALL_ACCESS)
                regDefaultIconKey = winreg.CreateKeyEx(regMainKey, "DefaultIcon", 0, winreg.KEY_ALL_ACCESS)
                regShellKey = winreg.CreateKeyEx(regMainKey, "shell\open\command", 0, winreg.KEY_ALL_ACCESS)

                winreg.SetValueEx(regMainKey, None, 0, winreg.REG_SZ, "Retrocraft Launcher Protocol")
                winreg.SetValueEx(regMainKey, "URL Protocol", 0, winreg.REG_SZ, "")
                winreg.SetValueEx(regDefaultIconKey, None, 0, winreg.REG_SZ, os.path.join(window.tbInstallPath.text(), "RetrocraftLauncher.exe"))
                winreg.SetValueEx(regShellKey, None, 0, winreg.REG_SZ, "\"" + os.path.join(window.tbInstallPath.text(), "RetrocraftLauncher.exe") + "\" \"%1\"")
            except WindowsError:
                errorDialog("Unable to create registry keys,\napplication or user may have insufficient privilleges!\n\nAborting installation!")
                window.logMessage("Unable to create registry keys!", 1)
                return
        elif(isMac):
            window.logMessage("Mac support is not yet available, aborting...", 1)
            #raise NotImplemented()
            return
        elif(isLinux):
            try:
                #Nix protocol Handler
                window.logMessage("Installing protocol handler...")
                appSharePath = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
                os.makedirs(appSharePath, exist_ok=True)
                f = open(os.path.join(appSharePath, "retrocraft.desktop"), "w+")
                lines = ["[Desktop Entry]", "Name=Retrocraft Launcher Protocol", "GenericName=Retrocraft Launcher Protocol", "Comment=Fast way to generate mptickets from URIs", "Exec="+Config.installPath()+"/RetrocraftLauncher \"%u\"", "Terminal=false", "Type=Application", "MimeType=x-scheme-handler/retrocraft;", "Categories=Application;"]
                f.write("\n".join(lines))
                f.flush()
                f.close()

                window.logMessage("Refreshing handler database...")
                if(subprocess.call(['update-desktop-database ~/.local/share/applications']) != 0):
                    errorDialog("Failed to update desktop database.")
                    window.logMessage("Failed to update desktop database.", 1)
                window.logMessage("Applying MIME settings...")
                if(subprocess.call(['xdg-mime default retrocraft.desktop x-scheme-handler/retrocraft;']) != 0):
                    errorDialog("Failed to register mime type.")
                    window.logMessage("Failed to register mime type.", 1)

                window.logMessage("This process hasn't been thoroughly tested, it may or may not work. Best way to test is using 'xdg-open retrocraft://...', if this opens the launcher then the desktop settings applied successfully. However your web-browser may require special configuration.")
                #infoDialog("This process hasn't been thoroughly tested, it may or may not work.\n\nBest way to test is using 'xdg-open retrocraft://...', if this opens the launcher\nthen the desktop settings applied successfully.\n\nHowever your web-browser may require special configuration.")
            except:
                errorDialog("Unable to create protocol handler desktop entry.")
                window.logMessage("Unable to create protocol handler desktop entry.", 1)
                return
            #end try
        else:
            raise NotImplemented()
            return
        #endif

        try:
            bundlePath = None
            if(hasattr(sys, "_MEIPASS")):
                bundlePath = os.path.abspath(sys._MEIPASS) # Preferred
            elif(os.environ.get("_MEIPASS")!=None):
                bundlePath = os.path.abspath(os.environ.get("_MEIPASS")) # Not sure if this is ever used
            elif(os.environ.get("_MEIPASS2")!=None):
                bundlePath = os.path.abspath(os.environ.get("_MEIPASS2")) # Older version of pyinstaller may use this?
            else:
                errorDialog("Unable to allocate temporary working directory.\n\nInstallation aborted!")
                window.logMessage("Unable to allocate temporary working directory!", 1)
                return
            #end try

            window.logMessage("Preparing install...")
            os.makedirs(Config.installPath(), exist_ok=True)

            exe = None
            if(isWindows):
                exe = "RetrocraftLauncher.exe"
            elif(isMac):
                exe = "RetrocraftLauncher.app"
            else:
                exe = "RetrocraftLauncher"
            #end if

            window.logMessage("Copying data files...")
            shutil.copyfile(os.path.abspath(os.path.join(bundlePath, exe)), os.path.abspath(os.path.join(Config.installPath(), exe)))
        except OSError:
            errorDialog("Unable to install executable in selected install path.\nApplication or user may have insufficient privilleges.\n\nInstallation aborted.")
            window.logMessage("Unable to install executable in selected install path.", 1)
            return
        except:
            errorDialog("Unspecified error occurred when copying data.\n\nInstallation aborted.")
            window.logMessage("Unspecified error occurred when copying data.", 1)
            return
        #end try

        infoDialog("Installation completed!")
        window.logMessage("Installation completed!")
        return
    else:
        infoDialog("Installation aborted!")
    #end if
#end def

def installLauncher(self):
    raise NotImplemented()
#end def

def installProfile(self):
    raise NotImplemented()
#end def

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
