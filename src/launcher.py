#!/usr/bin/env python3

import sys
import os
import platform
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

    tbServerIP = None
    tbServerPort = None
    tbMppass = None
    dlVersion = None

    def __init__(self):
        super().__init__()
        self.init_ui()
    #end def

    def init_ui(self):

        if(not Config.exists()):
            errorDialog("Settings file is missing,\n\n program may not have installed properly.")
            sys.exit()
        #end if

        self.setWindowTitle("Retrocraft Launcher")
        self.setFixedSize(480,0)

        vbox = QtWidgets.QVBoxLayout()

        lbTitle = QtWidgets.QLabel()
        lbTitle.setText("Retrocraft Launcher")
        lbTitle.setFont(Qt.QFont("Microsoft Sans Serif", 16))
        lbTitle.setMargin(10)

        pnServerSettings = QtWidgets.QGroupBox()
        pnServerSettings.setTitle("Direct Connection Settings")

        vboxServerSettings = QtWidgets.QVBoxLayout()
        hboxServerSettings = QtWidgets.QHBoxLayout()
        lbServerIP = QtWidgets.QLabel()
        lbServerIP.setText("IP Address:")
        lbServerIP.setFixedWidth(60)
        lbServerIP.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tbServerIP = QtWidgets.QLineEdit()
        lbServerPort = QtWidgets.QLabel()
        lbServerPort.setText("Port:")
        lbServerPort.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tbServerPort = QtWidgets.QLineEdit()
        hboxServerSettings.addWidget(lbServerIP)
        hboxServerSettings.addWidget(self.tbServerIP)
        hboxServerSettings.addWidget(lbServerPort)
        hboxServerSettings.addWidget(self.tbServerPort)

        hboxMppassSettings = QtWidgets.QHBoxLayout()
        lbMppass = QtWidgets.QLabel()
        lbMppass.setText("MP Pass:")
        lbMppass.setFixedWidth(60)
        lbMppass.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tbMppass = QtWidgets.QLineEdit()
        hboxMppassSettings.addWidget(lbMppass)
        hboxMppassSettings.addWidget(self.tbMppass)

        hboxVersionSettings = QtWidgets.QHBoxLayout()
        lbVersion = QtWidgets.QLabel()
        lbVersion.setText("Version:")
        lbVersion.setFixedWidth(60)
        lbVersion.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dlVersion = QtWidgets.QComboBox()
        self.dlVersion.addItems([d for d in os.listdir(os.path.join(Config.multiMcPath(), "instances")) if d != "_MMC_TEMP" and os.path.isdir(os.path.join(Config.multiMcPath(), "instances", d))])
        hboxVersionSettings.addWidget(lbVersion)
        hboxVersionSettings.addWidget(self.dlVersion)

        hboxDCInteractions = QtWidgets.QHBoxLayout()
        btnGenerateTicket = QtWidgets.QPushButton()
        btnGenerateTicket.setText("Connect")
        btnGenerateTicket.clicked.connect(self.generateTicket)
        hboxDCInteractions.addStretch()
        hboxDCInteractions.addWidget(btnGenerateTicket)

        vboxServerSettings.addLayout(hboxServerSettings)
        vboxServerSettings.addLayout(hboxMppassSettings)
        vboxServerSettings.addLayout(hboxVersionSettings)
        vboxServerSettings.addLayout(hboxDCInteractions)

        pnServerSettings.setLayout(vboxServerSettings)

        vbox.addWidget(lbTitle)
        vbox.addWidget(pnServerSettings)
        vbox.addStretch()

        self.setLayout(vbox)
        self.show()
    #end def

    def generateTicket(self):
        launchMinecraft(self.tbServerIP.text(), self.tbServerPort.text(), self.dlVersion.currentText(), self.tbMppass.text())
    #end def
#end class

def launchMinecraft(ipaddr, port, version, mppass):
    try:
        mpticketFile = open(os.path.abspath(os.path.join(Config.multiMcPath(), "instances", version, "mpticket")), "w")
        mpticketFile.write(ipaddr + "\n") #ip
        mpticketFile.write(port + "\n") #port
        mpticketFile.write(mppass) #mppass
        mpticketFile.flush()
        mpticketFile.close()

        subprocess.run(os.path.abspath(os.path.join(Config.multiMcPath(), "MultiMC.exe")) + " -l \"" + version + "\"", shell=False, check=False)
        sys.exit()
    except FileNotFoundError:
        errorDialog("Unable to find configuration file,\n\nprogram may not have been installed properly.")
    except:
        errorDialog("Encountered unspecified error.")
    #end try
#end def

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

if(len(sys.argv)>1):
    print(sys.argv[1])
else:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
#end if

protocolString = sys.argv[1]
protocolString = protocolString.partition("retrocraft://")[2]
parameters = None

if(protocolString==""):
    print("Unexpected protocol format, malformed or wrong version")
    sys.exit()
else:
    parameters = protocolString.split("/")
    if(len(parameters)!=4):
        print("Wrong number of parameters in protocol data, malformed or wrong version")
        sys.exit()
    #end if

    mpticketFile = None
    instancePath = os.path.abspath(os.path.join(Config.multiMcPath(), "instances", parameters[2]))
    if(os.path.exists(instancePath)==False):
        print("You do not have this version of Minecraft installed")
        sys.exit()
    else:
        launchMinecraft(parameters[0], parameters[1], parameters[2], parameters[3])
    #end if
#end if
