#!/usr/bin/env python3

import sys
import os
import platform
import time
import distutils
import PyQt5
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets

if(platform.system() == "Windows"):
    import winreg
#end if

configInstallPath = ""
configMultiMCPath = ""
configOverwriteExisting = ""

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

    def logMessage(self, message, level):
        if(level == 1):
            self.tbLogWindow.append("<span style='color:red'>" + message + "</span>")
        else:
            self.tbLogWindow.append("<span>" + message + "</span>")
    #end def

    def selectInstallPath(self):
        if (self.tbInstallPath.text()!=""):
            self.fioInstallPath.setDirectory(os.path.abspath(os.path.join(self.tbInstallPath.text(), "..")))
            #except: pass
        self.fioInstallPath.setFileMode(4)
        self.fioInstallPath.setWindowModality(QtCore.Qt.ApplicationModal)
        # Blocks main thread execution
        if(self.fioInstallPath.exec_()==1):
            # Seems like a really shitty way to do this
            self.tbInstallPath.setText(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], "RetrocraftLauncher")))
    #end def

    def selectMultiMCPath(self):
        if (self.tbMultiMCPath.text()!=""):
            self.fioInstallPath.setDirectory(os.path.abspath(os.path.join(self.tbMultiMCPath.text(), "..")))
            #except: pass
        self.fioInstallPath.setFileMode(4)
        self.fioInstallPath.setWindowModality(QtCore.Qt.ApplicationModal)
        # Blocks main thread execution
        if(self.fioInstallPath.exec_()==1):
            if(os.path.exists(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], "MultiMC.exe"))) and os.path.isfile(os.path.abspath(os.path.join(self.fioInstallPath.selectedFiles()[0], "MultiMC.exe")))):
                # Seems like a really shitty way to do this
                self.tbMultiMCPath.setText(os.path.abspath(self.fioInstallPath.selectedFiles()[0]))
            else:
                errorDialog("Unable to find MultiMC executable.\n\nSelect the base MultiMC directory containing,\nthe MultiMC executable file.")
    #end def
#end class

def errorDialog(message):
    dlg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error", message, QtWidgets.QMessageBox.Ok)
    dlg.exec_()
#end def

def installLauncher(self):

#end def

def installProfile(self):

#end def

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
