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


matplotlib.use("Qt5Agg")
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
            self._canvas.callbacks.connect("event", self.on_figure_event)
            self._toolbar = NavigationToolbar(self._canvas, self.MAIN_WIN)
            #
            self._container.addWidget(self._toolbar)
            self._container.addWidget(self._canvas)

            self._axes = self._figure.subplots(3, 1, sharex=True)
            self._ax_force = self._axes[0]
            self._ax_torque = self._axes[1]
            self._ax_scalar = self._axes[2]
            #
            for _ax in self._axes:
                _ax.callbacks.connect("ylim_changed", self._on_ylim_changed)
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
            self._x_data_list = []

            (self._line_actual_fx,) = self._ax_force.plot([], [], color="red", label="Fx")
            (self._line_actual_fy,) = self._ax_force.plot([], [], color="green", label="Fy")
            (self._line_actual_fz,) = self._ax_force.plot([], [], color="blue", label="Fz")

            (self._line_actual_tx,) = self._ax_torque.plot([], [], color="red", label="Tx")
            (self._line_actual_ty,) = self._ax_torque.plot([], [], color="green", label="Ty")
            (self._line_actual_tz,) = self._ax_torque.plot([], [], color="blue", label="Tz")

            (self._line_actual_scalar,) = self._ax_scalar.plot([], [], label="Scalar")

            self._ax_force.legend()
            self._ax_torque.legend()
            self._ax_scalar.legend()
            #
            self._enable_plotting = False

            # Plotting ----------------------------------------------------------------------------
            self._thread_plot = None

            # UR ----------------------------------------------------------------------------------
            self.MAIN_WIN._ur.connectedSignal.connect(self.onConnectedChanged)

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

    # Function to update the plot
    def _update_force(self):
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
                # console.log("changing y-max")
                self._force_max = y_max
                _should_update_y_lims = True

            if y_min < self._force_min:
                # console.log("changing y-min")

                self._force_min = y_min
                _should_update_y_lims = True

            if _should_update_y_lims:
                # console.log(y_min, y_max)
                self._ax_force.set_ylim(self._force_min, self._force_max)

    # Function to update the plot
    def _update_torque(self):
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

    def _update_scalar(self):
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
    def _thread_update_charts(self):
        #
        def task():
            #
            console.log("Thread `_thread_update_charts` has began!", style="success")
            #
            while self._enable_plotting:
                #     console.log("thread_update_charts")
                self._update_torque()
                self._update_scalar()
                self._update_force()
                #
                self._canvas.draw()
                #
                time.sleep(0.01)
            #
            console.log("Thread `_thread_update_charts` has stopped!", style="warning")

        #
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        #
        return thread

    # #############################################################################################
    # Figure Events ###############################################################################
    # #############################################################################################
    def _on_ylim_changed(self, ax):
        #
        _ax = ax
        # Y-axis limits changed, perform your desired action here
        _ax_idx = self._figure.axes.index(_ax)

        # Retrieve the y-axis limits
        ymin, ymax = _ax.get_ylim()

        if _ax_idx == 0:
            # console.log(f"({self._force_min}, {self._force_max}) - ({ymin}, {ymax})")
            self._force_min = ymin if ymin > self._force_min else self._force_min
            self._force_max = ymax if ymax < self._force_max else self._force_max
        elif _ax_idx == 1:
            self._torque_min = ymin if ymin > self._torque_min else self._torque_min
            self._torque_max = ymax if ymax < self._torque_max else self._torque_max
        elif _ax_idx == 2:
            self._scalar_min = ymin if ymin > self._scalar_min else self._scalar_min
            self._scalar_max = ymax if ymax < self._scalar_max else self._scalar_max

        print("Y-axis limits changed", _ax_idx)

    def on_figure_event(self, event):
        console.log("on_figure_event")
        # if event.name == 'draw_event':
        #     current_figure_options = self.get_figure_options()
        #     if current_figure_options != self._prev_figure_options:
        #         self._prev_figure_options = current_figure_options
        #         self.figure.canvas.callbacks.process(FigureOptionChangeEvent())
        # elif event.name == 'figure_option_change_event':
        #     # Handle the figure option change event
        #     print("Figure option has been changed!")
        #     # Perform any necessary actions here

    # UR RTDE #####################################################################################
    def onConnectedChanged(self, connected):
        #
        try:
            #
            func_name = "onConnectedChanged"
            LABEL = f"{module_name}/{func_name}"
            #
            console.log(f"{LABEL} :: onConnectedChanged:", connected)
            # return None
            #
            if connected == True:
                self._enable_plotting = connected
                self._thread_plot = self._thread_update_charts()
            else:
                self._enable_plotting = False
                self._thread_plot.join()

        except Exception as err:
            #
            console.print_exception()
