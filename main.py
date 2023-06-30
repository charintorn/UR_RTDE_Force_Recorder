# Modules
import sys
import threading

# QT5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
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
from gui.main_ui import Ui_MainWindow

# Others
from modules.rich_setup import *


# Modules
from modules.MatplotlibActualFT import MatplotlibActualFT
from modules.UrRTDE import UrRTDE
from modules.FileManager import FileManager

#
module_name = "main_win"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #
        func_name = "__init__"
        LABEL = f"{module_name}/{func_name}"
        #
        self.setupUi(self)

        # UR RTDE #################################################################################
        self._ur = UrRTDE(self)
        self._ur_connected = False
        self._ur.connectedSignal.connect(self.onConnectedChanged)
        # self._ur.rtdeFetchedSignal.connect(lambda data: console.log(data))

        # Matplotlib ##############################################################################
        self._actual_ft_matplot = MatplotlibActualFT(self)

        # Matplotlib ##############################################################################
        self.FILE_MANAGER = FileManager(self)

        self._update_ui()

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     self._actual_ft_matplot._figure.tight_layout()
    #     self._actual_ft_matplot._canvas.draw()

    def onConnectedChanged(self, status):
        #
        console.log("onConnectedChanged:", status)
        #
        self._ur_connected = status
        #
        self._update_ui()

    def _update_ui(self):
        #
        _inv_ui_list = [
            self.lineEdit_ip,
            self.comboBox_frequency,
            self.lineEdit_saveFilePath,
            self.pushButton_browse,
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
