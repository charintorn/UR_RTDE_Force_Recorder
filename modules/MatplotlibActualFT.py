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

            # -- Parent refs -- #
            self.MAIN_WIN = main_win
            self.UR = self.MAIN_WIN._ur
            #
            self._container = self.MAIN_WIN.verticalLayout_actualFT
            # -- Attributes -- #

            # -- Local refs -- #

            # -- Actions -- #

            # -- Emitters -- #

            # -- Signals -- #

            # -- Initialize -- #
            #
            self._figure = matplotlib.figure.Figure()
            self._canvas = FigureCanvas(self._figure)
            self._toolbar = NavigationToolbar(self._canvas, self.MAIN_WIN)
            #
            self._container.addWidget(self._toolbar)
            self._container.addWidget(self._canvas)

            self._axes = self._figure.subplots(3, 1, sharex=True)
            #

            self._x_axis_range = 100
            self._force_max = 1
            self._force_min = 0
            # self._force_axes = []
            # self._torque_axes = []
            #

            self.update_ylabels()

            # Tighten the layout
            self._figure.tight_layout()

            # Create an empty line object
            self.new_x = 0
            self.x = []
            self.y = []

            (self.line,) = self._axes[0].plot([], [])
            # (self._line_Fx,) = self._axes[0].plot(self.UR.timstamp_list, self.UR.actual_tcp_Fx)
            # Set up the plot axes
            self._axes[0].set_xlim(0, 100)
            # self._axes[0].set_ylim(-100, 100)

            # Update the plot
            # self._canvas.draw()

            # self.ani = animation.FuncAnimation(self._figure, self.animation_callback, interval=250)
            self.ani = animation.FuncAnimation(self._figure, self.update, interval=10)

        except Exception as err:
            #
            console.print_exception()

        # self.mpl_canvas.draw_idle()

        # Enable mouse scrolling for zooming
        # self.mpl_canvas.mpl_connect("scroll_event", self.on_scroll)

    # Function to generate new data
    def generate_data(self):
        self.y = np.array(self.UR.actual_tcp_Fx)
        self.x = np.arange(0, len(self.UR.get_timeframe()), 1)
        # self.y = np.arange(0, len(self.UR.get_timeframe()), 1)

    # Function to update the plot
    def update(self, frame):
        self.generate_data()
        # console.log("self.x:", self.x)
        # console.log("self.y:", self.y)
        # console.log("self.UR.timstamp_list:", self.UR.timstamp_list)
        # console.log("self.UR.actual_tcp_Fxt:", self.UR.actual_tcp_Fx)

        # self.line.set_data(self.UR.timstamp_list, self.UR.actual_tcp_Fx)
        self.line.set_data(self.x, self.y)

        if len(self.x) > 100:
            self._axes[0].set_xlim(len(self.x) - self._x_axis_range, len(self.x))
        else:
            self._axes[0].set_xlim(0, self._x_axis_range)

        # y-axis, Calculate the minimum and maximum y-values within the time frame
        def get_max(x_list):
            if len(x_list) >= self._x_axis_range:
                lastest_elements = x_list[-1 * self._x_axis_range :]
                return max(lastest_elements)
            elif len(x_list) > 0:
                return max(x_list)
            else:
                return 1

        def get_min(x_list):
            if len(x_list) >= self._x_axis_range:
                lastest_elements = x_list[-1 * self._x_axis_range :]
                return min(lastest_elements)
            elif len(x_list) > 0:
                return min(x_list)
            else:
                return 0

        y_max = get_max(self.UR.actual_tcp_Fx)
        y_min = get_min(self.UR.actual_tcp_Fx)

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
            self._axes[0].set_ylim(self._force_min, self._force_max)

    def animation_callback(self, i):
        # self._feedback_position_list
        console.log("animation_callback - ", i, len(self.UR.timstamp_list), len(self.UR.actual_tcp_Fx))
        #
        self._line_Fx.set_data(self.UR.timstamp_list, self.UR.actual_tcp_Fx)
        self._axes[0].set_xlim(max(0, len(self.UR.timstamp_list) - 10), len(self.UR.timstamp_list))

        # _timestamp_list = self.UR.timstamp_list
        # _actual_tcp_Fx = self.UR.actual_tcp_Fx
        # #
        # console.log("_timestamp_list:", _timestamp_list.__len__())
        # console.log("_actual_tcp_Fx:", _actual_tcp_Fx.__len__())
        # # console.log("_actual_tcp_force_list:", _actual_tcp_force_list)
        # self.update_charts(
        #     x_axis_data=_timestamp_list,
        #     ax0_data=_actual_tcp_Fx,
        #     # ax2_data=self._feedback_velocity_list,
        #     # ax4_data=self._feedback_torque_list,
        # )

    def update_ylabels(self):
        try:
            #
            func_name = "update_ylabels"
            LABEL = f"{module_name}/{func_name}"
            #        s
            self._axes[0].set_ylabel("Force (N)", labelpad=20)
            self._axes[1].set_ylabel("Torque (Nm)", labelpad=20)
            self._axes[2].set_ylabel("Force (scalar)", labelpad=20)

            self._axes[2].set_xlabel("timestamp", labelpad=0)

            for _axs in self._axes:
                _axs.grid(True)

        except Exception as err:
            #
            console.print_exception()

    def update_charts(self, x_axis_data=[], ax0_data=[], ax1_data=[], ax2_data=[]):
        # Update axes[0]
        # self._axes[0].clear()  # Clear the previous data
        self._axes[0].plot(x_axis_data, ax0_data, "-", color="red")  # Plot new data

        # # Update axes[1]
        # self._axes[1].clear()  # Clear the previous data
        # self._axes[1].plot(x_axis_data, ax1_data, "-", color="green")  # Plot new data

        # self._axes[3].clear()  # Clear the previous data
        # self._axes[2].plot(x_axis_data, ax2_data, "-", color="blue")  # Plot new data

        # self.update_ylabels()

        #
        self._canvas.draw()  # Redraw the canvas to reflect the changes
        # self.mpl_canvas.draw_idle()
