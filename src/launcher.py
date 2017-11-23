#!/usr/bin/env python3

import sys
import os
import platform
import distutils
import subprocess
import PyQt5
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets

if(platform.system() == "Windows"):
    import winreg
#end if

configMultiMCPath = "C:\\Users\\Zuriki\\Documents\\multimc"

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.show()
    #end def
#end class

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
        mpticketFile = open(os.path.abspath(os.path.join(instancePath, "mpticket")), "w")
        mpticketFile.write(parameters[0] + "\n") #ip
        mpticketFile.write(parameters[1] + "\n") #port
        mpticketFile.write(parameters[3]) #mppass
        mpticketFile.flush()
        mpticketFile.close()

        subprocess.run(os.path.abspath(os.path.join(configMultiMCPath, "MultiMC.exe")) + " -l \"" + parameters[2] + "\"", shell=False, check=False)
    #end if
#end if
