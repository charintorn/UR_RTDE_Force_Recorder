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
from PyQt5.QtWidgets import QFileDialog


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

            # Initialize ##########################################################################

        except Exception as err:
            #
            console.print_exception()

    # #############################################################################################
    # Browse Save Directory #######################################################################
    # #############################################################################################
    def open_directory_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            self.MAIN_WIN, "Select Save Directory", self._save_dir, options=options
        )

        if directory:
            # console.log("Selected directory:", directory)
            self.changeSaveDirectory(directory)

    def changeSaveDirectory(self, dir_path_str):
        self._save_dir = dir_path_str

    # #############################################################################################
    # Save ########################################################################################
    # #############################################################################################
    def _on_save_handler(self):
        # Open a dialog to browse for the save directory
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        save_directory = QFileDialog.getExistingDirectory(self.MAIN_WIN, "Select Save Directory", options=options)

        if save_directory:
            data = self.UR.get_data_record()
            # console.log("save_record:", data)

            # Generate the file name based on the current date and time
            current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = f"record_{current_datetime}.csv"

            # Create the full path by joining the save directory and the filename
            save_path = os.path.join(self._save_dir, filename)

            self.save_data_to_csv(data, save_path)

    def save_data_to_csv(self, data, file_path):
        console.log("save_data_to_csv")
        console.log("- file_path:", file_path)
        console.log("- data:", data)
        # Write the data to a CSV file
        with open(file_path, "w") as file:
            # Write the header row
            header = ",".join(data.keys())
            file.write(header + "\n")

            # Write the data rows
            for i in range(len(data["timestamp"])):
                row_values = [str(data[key][i]) for key in data.keys()]
                row = ",".join(row_values)
                file.write(row + "\n")

        # Open the CSV file in write mode
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write the header row with the keys
            writer.writerow(data.keys())
            # Write the data rows
            for i in range(num_rows):
                row = [values[j][i] for j in range(len(keys))]
                writer.writerow(row)
        print(f"Data written to {file_path}")
        pass
