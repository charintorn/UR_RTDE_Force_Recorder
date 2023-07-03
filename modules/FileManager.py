# Modules
import sys
import os
import threading
import time
import re
import math
from enum import Enum
import csv
from datetime import datetime

# QT5
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# Others
from modules.rich_setup import *

module_name = "FileManager"


class FileManager(QObject):
    # #############################################################################################
    # __init__ ####################################################################################
    # #############################################################################################
    def __init__(self, main_win) -> None:
        try:
            super().__init__()
            #
            func_name = "__init__"
            LABEL = f"{module_name}/{func_name}"
            console.log(LABEL, style="info")
            #

            # Parent refs #########################################################################
            self.MAIN_WIN = main_win
            self.UR = self.MAIN_WIN._ur

            # Attributes ##########################################################################
            # Save #
            self._save_dir = ""
            file_directory = os.path.dirname(os.path.abspath(__file__))
            parent_directory = os.path.abspath(os.path.join(file_directory, ".."))
            self.changeSaveDirectory(parent_directory)

            # Local refs ##########################################################################

            # Actions #############################################################################

            # Emitters ############################################################################

            # Signals #############################################################################
            self.MAIN_WIN.pushButton_save.clicked.connect(self._on_save_handler)
            self.MAIN_WIN.actionSave.triggered.connect(self._on_save_handler)

            # Initialize ##########################################################################

        except Exception as err:
            #
            console.print_exception()

    # #############################################################################################
    # Save ########################################################################################
    # #############################################################################################
    def _on_save_handler(self):
        # Generate the file name based on the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"record_{current_datetime}.csv"

        # Open a dialog to browse for the save directory and specify the default file name
        file_path, _ = QFileDialog.getSaveFileName(
            self.MAIN_WIN, "Save File", os.path.join(self._save_dir, filename), "CSV Files (*.csv)"
        )

        if file_path:
            # Set the save directory based on the selected file path
            self.changeSaveDirectory(os.path.dirname(file_path))

            # Save the record to the specified file
            self.save_record(file_path)

    def changeSaveDirectory(self, dir_path_str):
        self._save_dir = dir_path_str

    def save_record(self, file_path):
        data = self.UR.get_data_record()
        # console.log("save_record:", data)

        # Extract the keys from the dictionary
        keys = list(data.keys())

        # Extract the values from the dictionary
        values = list(data.values())

        # Determine the number of rows in the CSV file
        num_rows = len(values[0])

        # Open the CSV file in write mode
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write the header row with the keys
            writer.writerow(keys)

            # Write the data rows
            for i in range(num_rows):
                row = [values[j][i] for j in range(len(keys))]
                writer.writerow(row)

        console.log(f"Data written to {file_path}")
        # Show a dialog indicating that the file has been saved
        QMessageBox.information(self.MAIN_WIN, "File Saved", f"The file has been saved at:\n{file_path}")
