# Modules
import sys
import os
import threading


# Add "./modules" to the Python module search path
# sys.path.append("./modules")
# sys.path.append("./modules/rtde")

sys.path.append(os.path.join(os.getcwd(), "modules"))

MODULES_PATH = os.path.join(os.getcwd(), "modules")
print("MODULES_PATH:", MODULES_PATH)

# QT5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer


# Matplotlib
import numpy as np
import matplotlib

# matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.figure


# UI
from gui.resources import resources_rc
from gui.main_ui import Ui_MainWindow

# Others
from modules.rich_setup import *


# Modules
from modules.DialogManager import DialogManager
from modules.MatplotlibActualFT import MatplotlibActualFT
from modules.UrRTDE import UrRTDE
from modules.FileManager import FileManager

#
module_name = "main_win"


class MainWindow(QMainWindow, Ui_MainWindow):
    # #############################################################################################
    # __init__ ####################################################################################
    # #############################################################################################
    def __init__(self):
        QMainWindow.__init__(self)
        #
        func_name = "__init__"
        LABEL = f"{module_name}/{func_name}"
        #
        self.setupUi(self)

        # Infomation ##############################################################################
        self.APP_NAME = "UR Force Recorder"
        self.VERSION = "0.1.0"

        # Application #############################################################################
        self.actionExit.triggered.connect(self._close_app)

        # Dialog Manager ##########################################################################
        self.DIALOG_MANAGER = DialogManager(self)

        # UR RTDE #################################################################################
        self._ur = UrRTDE(self)
        self._ur_connected = False
        self._ur.connectedSignal.connect(self.onConnectedChanged)
        # self._ur.rtdeFetchedSignal.connect(lambda data: console.log(data))

        # Matplotlib ##############################################################################
        self._actual_ft_matplot = MatplotlibActualFT(self)

        # File manager ############################################################################
        self.FILE_MANAGER = FileManager(self)

        # UIs #####################################################################################
        self._init_ui()
        self._update_ui()

    # #############################################################################################
    # Application #################################################################################
    # #############################################################################################
    def _close_app(self):
        QApplication.quit()

    # #############################################################################################
    # UIs #########################################################################################
    # #############################################################################################
    def _init_ui(self):
        self.setWindowTitle(f"{self.APP_NAME} - Version {self.VERSION}")

    def _update_ui(self):
        #
        _inv_ui_list = [
            self.lineEdit_ip,
            self.comboBox_frequency,
            self.pushButton_save,
        ]
        #
        _enable = not self._ur_connected
        _start_btn_text = "Start" if not self._ur_connected else "Stop"
        _start_btn_colour = "" if not self._ur_connected else "red"

        for _ui in _inv_ui_list:
            _ui.setEnabled(_enable)
        #
        self.pushButton_start.setText(_start_btn_text)
        self.pushButton_start.setStyleSheet(f"background-color:{_start_btn_colour}")

    # #############################################################################################
    # Connection ##################################################################################
    # #############################################################################################
    def onConnectedChanged(self, status):
        #
        console.log("onConnectedChanged:", status)
        #
        self._ur_connected = status
        #
        self._update_ui()


# #################################################################################################
# __main__ ########################################################################################
# #################################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
