# Modules
import sys
import os
import threading
import time
import re
import math
from enum import Enum

# Matplotlib
import numpy as np
import matplotlib

# matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.figure

# QT5
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

# RTDE
import modules.rtde.rtde as rtde
import modules.rtde.rtde_config as rtde_config

# Others
from modules.rich_setup import *

module_name = "UrRTDE"


class UrRTDE(QObject):
    connectedSignal = pyqtSignal(bool)
    rtdeFetchedSignal = pyqtSignal(dict)

    #
    def __init__(self, main_win) -> None:
        try:
            super().__init__()
            #
            func_name = "__init__"
            LABEL = f"{module_name}/{func_name}"
            #

            # -- Parent refs -- #
            self.MAIN_WIN = main_win

            # -- Attributes -- #
            # data #
            self.timstamp_list = []
            self.actual_tcp_force_list = []  # list of vector6D
            self.actual_tcp_Fx = []
            self.actual_tcp_Fy = []
            self.actual_tcp_Fz = []
            self.actual_tcp_Tx = []
            self.actual_tcp_Ty = []
            self.actual_tcp_Tz = []

            # RTDE #
            self._CONFIG_FILE = "rtde_config.xml"
            self._conf = None
            #
            self._state_names = None
            self._state_types = None
            #
            self._setp_names = None
            self._setp_types = None
            #
            self._watchdog_names = None
            self._watchdog_types = None
            #
            self._read_thread = None
            self._read_thread_running = False

            # Connected #
            self._ip = self.MAIN_WIN.lineEdit_ip.text().replace(" ", "")
            self._port = 30004
            self._connected = False
            self._rtde_connection = rtde.RTDE(self._ip, self._port)
            #
            self.MAIN_WIN.comboBox_frequency.setCurrentIndex(5)
            self._freq = self.freqComboboxTextChanged(self.MAIN_WIN.comboBox_frequency.currentText())

            #

            # -- Local refs -- #

            # -- Actions -- #

            # -- Emitters -- #

            # -- Signals -- #
            # connection
            self.MAIN_WIN.lineEdit_ip.textChanged.connect(self.changeIp)
            self.MAIN_WIN.pushButton_start.clicked.connect(self.onStartBtnClicked)
            # frequency
            self.MAIN_WIN.comboBox_frequency.currentTextChanged.connect(self.freqComboboxTextChanged)
            # RTDE
            self.rtdeFetchedSignal.connect(self.rtde_fetched)

            # -- Initialize -- #
            self.init_rtde()

        except Exception as err:
            #
            console.print_exception()

    # Frequency ###################################################################################
    def freqComboboxTextChanged(self, text):
        _freq = self.extractFreqFromText(text)
        return self.changeFreq(_freq)

    def extractFreqFromText(self, frequency_string):
        pattern = r"(\d+(\.\d+)?)\s*(Hz|GHz)"
        match = re.match(pattern, frequency_string, re.IGNORECASE)

        if match:
            value = float(match.group(1))
            unit = match.group(3)

            if unit.lower() == "ghz":
                value *= 1e9
            elif unit.lower() == "hz":
                value *= 1

            return value
        else:
            return None

    def changeFreq(self, freq):
        #
        self._freq = freq

        #
        console.log("changeFreq:", self._freq)
        #
        return self._freq

    # Connection ##################################################################################
    def changeIp(self, ip_str):
        self._ip = ip_str.replace(" ", "")
        # console.log("changeIp:", self._ip)
        #
        self._rtde_connection = rtde.RTDE(self._ip, self._port)

    def onStartBtnClicked(self):
        if not self._connected:
            self.connect_ur()

        else:
            self.disconnect()

    def connect_ur(self):
        try:
            #
            func_name = "connect"
            LABEL = f"{module_name}/{func_name}"
            console.log(LABEL, "connecting ...", style="success")
            #
            self._rtde_connection.connect()
            #
            # _controller_version = self._rtde_connection.get_controller_version()
            # print("controller_version:", _controller_version)
            #
            self._connected = True
            self.connectedSignal.emit(self._connected)
            console.log(LABEL, "connected.", style="success")
            #
            self.config_after_connected()
            #
            self._read_thread_running = self._connected
            self._read_thread = self.read()
            #

        except Exception as err:
            #
            console.print_exception()

    def disconnect(self):
        try:
            #
            func_name = "disconnecting"
            LABEL = f"{module_name}/{func_name}"
            console.log(LABEL, "disconnecting ...", style="error")
            #
            # first, stop read-thread
            self._read_thread_running = False
            self._read_thread.join()

            # disconnect from UR
            self._rtde_connection.disconnect()

            # emit the signal
            self._connected = False
            self.connectedSignal.emit(self._connected)
            #
            console.log(LABEL, "disconnected!", style="error")
            #

        except Exception as err:
            #
            console.print_exception()

    # RTDE ########################################################################################
    def init_rtde(self):
        # Get the path of the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the RTDE configuration file
        config_path = os.path.join(current_dir, self._CONFIG_FILE)

        # Configure the RTDE communication
        self._conf = rtde_config.ConfigFile(config_path)

        self._state_names, self._state_types = self._conf.get_recipe(
            "state"
        )  # Define recipe for access to robot output ex. joints,tcp etc.
        self._setp_names, self._setp_types = self._conf.get_recipe("setp")  # Define recipe for access to robot input
        self._watchdog_names, self._watchdog_types = self._conf.get_recipe("watchdog")

    def config_after_connected(self):
        # ------------------- setup recipes ----------------------------
        FREQUENCY = 50  # send data in 500 Hz instead of default 125Hz
        self._rtde_connection.send_output_setup(self._state_names, self._state_types, FREQUENCY)
        setp = self._rtde_connection.send_input_setup(
            self._setp_names, self._setp_types
        )  # Configure an input package that the external application will send to the robot controller
        watchdog = self._rtde_connection.send_input_setup(self._watchdog_names, self._watchdog_types)

    def read(self):
        #
        _freq = self._freq
        _T = (1 / _freq) * 0.8
        #

        def task():
            # start synchronizing
            if not self._rtde_connection.send_start():
                sys.exit()
            #
            while self._read_thread_running:
                # console.log("read")
                state = self._rtde_connection.receive()
                timestamp = state.timestamp
                actual_TCP_force = state.actual_TCP_force
                # print("timestamp:", timestamp, "\tactual_TCP_force:", actual_TCP_force)
                # console.log("actual_TCP_force:", actual_TCP_force)

                self.rtdeFetchedSignal.emit(
                    {
                        "timestamp": timestamp,
                        "actual_TCP_force": actual_TCP_force,
                    }
                )

                time.sleep(_T)

        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        #
        return thread

    def rtde_fetched(self, data):
        #
        # console.log("rtde_fetched:", data)
        #
        #
        timstamp = data["timestamp"]
        Fx = data["actual_TCP_force"][0]
        # console.log("Fx:", Fx)
        self.timstamp_list.append(timstamp)
        self.actual_tcp_Fx.append(Fx)
        self.actual_tcp_Fy.append(data["actual_TCP_force"][1])
        self.actual_tcp_Fz.append(data["actual_TCP_force"][2])
        self.actual_tcp_Tx.append(data["actual_TCP_force"][3])
        self.actual_tcp_Ty.append(data["actual_TCP_force"][4])
        self.actual_tcp_Tz.append(data["actual_TCP_force"][5])

    def get_timeframe(self):
        return self.timstamp_list

    def get_fx(self):
        return self.actual_tcp_Fx