import os
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

import re
from functools import partial


# custom modules #
from rich_setup import *

module_name = "modules/gui/background/image.py"


class ModeModule(QObject):
    def __init__(self, main_wn):
        super().__init__(main_wn)
        #
        func_name = "__init__"
        LABEL = f"{module_name}/{func_name}"
        #
        console.log(LABEL, style="info")
        #
        # -- Parent refs -- #
        self._main_wn = main_wn

        # -- Attributes -- #

        # -- Local refs -- #

        # -- Actions -- #

        # -- Emitters -- #

        # -- Signals -- #

        # -- Initialize -- #

    def _update_ui(self):
        try:
            #
            func_name = "_update_ui"
            LABEL = f"{module_name}/{func_name}"
            #
            # console.log(LABEL)
            #
            # -- Operate Here -- #

            pass

        except Exception as err:
            console.print_exception()
            self._main_wn.app_dialog_manager.error.show(err, LABEL)
