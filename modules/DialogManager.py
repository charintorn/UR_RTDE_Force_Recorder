from PyQt5.QtWidgets import QMessageBox

# custom modules #
from modules.rich_setup import *


module_name = "DialogManager"


class ErrorManager:
    def __init__(self) -> None:
        self.create_dialog()

    def create_dialog(self):
        try:
            self.dialog = QMessageBox()
            self.dialog.setIcon(QMessageBox.Critical)
            # self.dialog.setMinimumWidth(600)  # Set the minimum width of the dialog here
            # self.dialog.setStyleSheet("QLabel{min-width: 150px;}")

        except Exception as err:
            console.print_exception()

    def show(self, text="", title="Error", info=""):
        try:
            self.dialog.setText(str(text))
            self.dialog.setWindowTitle(str(title))
            self.dialog.setInformativeText(str(info))
            self.dialog.exec_()
        except Exception as err:
            console.print_exception()


class DialogManager:
    def __init__(self, main_win) -> None:
        try:
            #
            func_name = "__init__"
            LABEL = f"{module_name}::{func_name}"
            #
            console.log(LABEL, style="info")
            #
            self.MAIN_WIN = main_win
            self.error = ErrorManager()
            #
            # self.error.show("Custom Error!@#", "Test Error")
            pass
        except Exception as err:
            console.print_exception()
            # self.MAIN_WIN.DIALOG_MANAGER.error.show(err, LABEL)
