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

if(platform.system() == "Windows"):
    import winreg
#end if

configMultiMCPath = "C:\\Users\\Zuriki\\Documents\\multimc"

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
        self.dlVersion.addItems([d for d in os.listdir(os.path.join(configMultiMCPath, "instances")) if d != "_MMC_TEMP" and os.path.isdir(os.path.join(configMultiMCPath, "instances", d))])
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
    mpticketFile = open(os.path.abspath(os.path.join(configMultiMCPath, "instances", version, "mpticket")), "w")
    mpticketFile.write(ipaddr + "\n") #ip
    mpticketFile.write(port + "\n") #port
    mpticketFile.write(mppass) #mppass
    mpticketFile.flush()
    mpticketFile.close()

    subprocess.run(os.path.abspath(os.path.join(configMultiMCPath, "MultiMC.exe")) + " -l \"" + version + "\"", shell=False, check=False)
    sys.exit()
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
    instancePath = os.path.abspath(os.path.join(configMultiMCPath, "instances", parameters[2]))
    if(os.path.exists(instancePath)==False):
        print("You do not have this version of Minecraft installed")
        sys.exit()
    else:
        launchMinecraft(parameters[0], parameters[1], parameters[2], parameters[3])
    #end if
#end if
