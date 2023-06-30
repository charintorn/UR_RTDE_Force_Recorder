# Modules
import sys
import threading
import time
import math
from enum import Enum

# Matplotlib
import numpy as np
import matplotlib
import matplotlib.animation as animation


# matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.figure

# QT5
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

# Others
from modules.rich_setup import *

module_name = "MatplotlibActualFT"


class MatplotlibActualFT(QObject):
    def __init__(self, main_win) -> None:
        try:
            super().__init__()
            #
            func_name = "__init__"
            LABEL = f"{module_name}/{func_name}"
            #

            # Parent refs #########################################################################
            self.MAIN_WIN = main_win
            self.UR = self.MAIN_WIN._ur
            #
            self._container = self.MAIN_WIN.verticalLayout_actualFT
            # Attributes ##########################################################################

            # Local refs ##########################################################################

            # Actions #############################################################################

            # Emitters ############################################################################

            # Signals #############################################################################

            # Initialize ##########################################################################
            #
            self._figure = matplotlib.figure.Figure()
            self._canvas = FigureCanvas(self._figure)
            self._toolbar = NavigationToolbar(self._canvas, self.MAIN_WIN)
            #
            self._container.addWidget(self._toolbar)
            self._container.addWidget(self._canvas)

            self._axes = self._figure.subplots(3, 1, sharex=True)
            self._ax_force = self._axes[0]
            self._ax_torque = self._axes[1]
            self._ax_scalar = self._axes[2]
            #

            self._x_axis_range = 500
            #
            self._force_max = 1
            self._force_min = 0
            #
            self._torque_max = 1
            self._torque_min = 0
            #
            self._scalar_max = 1
            self._scalar_min = 0

            self._update_labels()

            # Tighten the layout
            self._figure.tight_layout()

            # Create an empty line object
            self.new_x = 0
            self._x_data_list = []
            self.y = []

            (self._line_actual_fx,) = self._ax_force.plot([], [], label="Fx")
            (self._line_actual_fy,) = self._ax_force.plot([], [], label="Fy")
            (self._line_actual_fz,) = self._ax_force.plot([], [], label="Fz")

            (self._line_actual_tx,) = self._ax_torque.plot([], [], label="Tx")
            (self._line_actual_ty,) = self._ax_torque.plot([], [], label="Ty")
            (self._line_actual_tz,) = self._ax_torque.plot([], [], label="Tz")

            (self._line_actual_scalar,) = self._ax_scalar.plot([], [], label="Scalar")

            self._ax_force.legend()
            self._ax_torque.legend()
            self._ax_scalar.legend()
            #
            self._enable_plotting = False

            # UR ----------------------------------------------------------------------------------
            self.MAIN_WIN._ur.connectedSignal.connect(self.onConnectedChanged)

            # self._animation_ft = animation.FuncAnimation(self._figure, self._update_charts, interval=10)

        except Exception as err:
            #
            console.print_exception()

    def _update_labels(self):
        try:
            #
            func_name = "update_ylabels"
            LABEL = f"{module_name}/{func_name}"
            #        s
            self._ax_force.set_ylabel("Force (N)", labelpad=20)
            self._axes[1].set_ylabel("Torque (Nm)", labelpad=20)
            self._axes[2].set_ylabel("Force (scalar)", labelpad=20)

            self._axes[2].set_xlabel("timestamp", labelpad=0)

            for _axs in self._axes:
                _axs.grid(True)

        except Exception as err:
            #
            console.print_exception()

    def get_min_max_in_range(self, y_list):
        #
        y_min = 0
        y_max = 0
        #
        if len(y_list) >= self._x_axis_range:
            #
            lastest_elements = y_list[-1 * self._x_axis_range :]
            #
            y_max = max(lastest_elements)
            y_min = min(lastest_elements)
            #
        elif len(y_list) > 0:
            #
            y_max = max(y_list)
            y_min = min(y_list)
            #
        else:
            #
            y_max = 1
            y_min = 0
        #
        return (y_min, y_max)

    def _update_charts(self, frame):
        self._update_force(frame)
        self._update_torque(frame)
        self._update_scalar(frame)

    # Function to update the plot
    def _update_force(self, frame):
        #
        _x_data_list = self.UR.pkg_count_list
        _fx_list = self.UR.actual_tcp_Fx
        _fy_list = self.UR.actual_tcp_Fy
        _fz_list = self.UR.actual_tcp_Fz

        # plot the data
        self._line_actual_fx.set_data(_x_data_list, _fx_list)
        self._line_actual_fy.set_data(_x_data_list, _fy_list)
        self._line_actual_fz.set_data(_x_data_list, _fz_list)

        # Adjust x-axist #
        if len(_x_data_list) > self._x_axis_range:
            self._ax_force.set_xlim(len(_x_data_list) - self._x_axis_range, len(_x_data_list))
        else:
            self._ax_force.set_xlim(0, self._x_axis_range)

        # y-axis, Calculate the minimum and maximum y-values within the time frame
        _y_data_lists = [_fx_list, _fy_list, _fz_list]

        for f_data in _y_data_lists:
            #
            y_min, y_max = self.get_min_max_in_range(f_data)
            #
            _should_update_y_lims = False

            if y_max > self._force_max:
                console.log("changing y-max")
                self._force_max = y_max
                _should_update_y_lims = True

            if y_min < self._force_min:
                console.log("changing y-min")

                self._force_min = y_min
                _should_update_y_lims = True

            if _should_update_y_lims:
                console.log(y_min, y_max)
                self._ax_force.set_ylim(self._force_min, self._force_max)

    # Function to update the plot
    def _update_torque(self, frame):
        #
        x_data_list = self.UR.pkg_count_list
        tx_list = self.UR.actual_tcp_Tx
        ty_list = self.UR.actual_tcp_Ty
        tz_list = self.UR.actual_tcp_Tz

        # plot the data
        self._line_actual_tx.set_data(x_data_list, tx_list)
        self._line_actual_ty.set_data(x_data_list, ty_list)
        self._line_actual_tz.set_data(x_data_list, tz_list)

        # Adjust x-axist #
        if len(x_data_list) > self._x_axis_range:
            self._ax_torque.set_xlim(len(x_data_list) - self._x_axis_range, len(x_data_list))
        else:
            self._ax_torque.set_xlim(0, self._x_axis_range)

        # y-axis, Calculate the minimum and maximum y-values within the time frame
        _y_data_lists = [tx_list, ty_list, tz_list]

        for f_data in _y_data_lists:
            #
            y_min, y_max = self.get_min_max_in_range(f_data)
            #
            _should_update_y_lims = False

            if y_max > self._torque_max:
                console.log("changing y-max")
                self._torque_max = y_max
                _should_update_y_lims = True

            if y_min < self._torque_min:
                console.log("changing y-min")

                self._torque_min = y_min
                _should_update_y_lims = True

            if _should_update_y_lims:
                console.log(y_min, y_max)
                self._ax_torque.set_ylim(self._torque_min, self._torque_max)

    def _update_scalar(self, frame):
        #
        x_data_list = self.UR.pkg_count_list
        force_list = self.UR.actual_tcp_scalar
        # console.log("force_list:", force_list.__len__())

        # plot the data
        self._line_actual_scalar.set_data(x_data_list, force_list)

        # Adjust x-axist #
        if len(x_data_list) > self._x_axis_range:
            self._ax_scalar.set_xlim(len(x_data_list) - self._x_axis_range, len(x_data_list))
        else:
            self._ax_scalar.set_xlim(0, self._x_axis_range)

        # y-axis, Calculate the minimum and maximum y-values within the time frame

        y_min, y_max = self.get_min_max_in_range(force_list)
        #
        _should_update_y_lims = False

        if y_max > self._scalar_max:
            console.log("changing y-max")
            self._scalar_max = y_max
            _should_update_y_lims = True

        if y_min < self._scalar_min:
            console.log("changing y-min")

            self._scalar_min = y_min
            _should_update_y_lims = True

        if _should_update_y_lims:
            console.log(y_min, y_max)
            self._ax_scalar.set_ylim(self._scalar_min, self._scalar_max)

    # Thread ######################################################################################
    def thread_update_charts(self):
        #
        def task():
            #
            while self._enable_plotting:
                console.log("thread_update_charts")
                time.sleep(0.1)

        #
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        #
        return thread

    # UR RTDE #####################################################################################
    def onConnectedChanged(self, connected):
        #
        try:
            #
            func_name = "onConnectedChanged"
            LABEL = f"{module_name}/{func_name}"
            #
            console.log(f"{LABEL} :: onConnectedChanged:", connected)
            #
            # self._ur_connected = connected
            self._enable_plotting = connected
            #

        except Exception as err:
            #
            console.print_exception()
