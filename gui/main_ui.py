# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1079, 793)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icon/icon/ur_logo.ico"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtWidgets.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_ipRow1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ipRow1.setObjectName("horizontalLayout_ipRow1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_ipRow1.addWidget(self.label)
        self.lineEdit_ip = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.horizontalLayout_ipRow1.addWidget(self.lineEdit_ip)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_ipRow1.addWidget(self.line_2)
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout_ipRow1.addWidget(self.pushButton_clear)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_ipRow1.addWidget(self.line_4)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_ipRow1.addWidget(self.label_2)
        self.comboBox_frequency = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_frequency.setObjectName("comboBox_frequency")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.comboBox_frequency.addItem("")
        self.horizontalLayout_ipRow1.addWidget(self.comboBox_frequency)
        self.checkBox_autoscroll = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_autoscroll.setEnabled(True)
        self.checkBox_autoscroll.setChecked(True)
        self.checkBox_autoscroll.setObjectName("checkBox_autoscroll")
        self.horizontalLayout_ipRow1.addWidget(self.checkBox_autoscroll)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_ipRow1.addWidget(self.line_3)
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_ipRow1.addWidget(self.pushButton_save)
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_ipRow1.addWidget(self.pushButton_start)
        self.verticalLayout_main.addLayout(self.horizontalLayout_ipRow1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_actualFT = QtWidgets.QWidget()
        self.tab_actualFT.setObjectName("tab_actualFT")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_actualFT)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_actualFT = QtWidgets.QVBoxLayout()
        self.verticalLayout_actualFT.setObjectName("verticalLayout_actualFT")
        self.verticalLayout_3.addLayout(self.verticalLayout_actualFT)
        self.tabWidget.addTab(self.tab_actualFT, "")
        self.tab_rawFT = QtWidgets.QWidget()
        self.tab_rawFT.setObjectName("tab_rawFT")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_rawFT)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_rawFT = QtWidgets.QVBoxLayout()
        self.verticalLayout_rawFT.setObjectName("verticalLayout_rawFT")
        self.verticalLayout_4.addLayout(self.verticalLayout_rawFT)
        self.tabWidget.addTab(self.tab_rawFT, "")
        self.tab_table = QtWidgets.QWidget()
        self.tab_table.setObjectName("tab_table")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_table)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea_table = QtWidgets.QScrollArea(self.tab_table)
        self.scrollArea_table.setWidgetResizable(True)
        self.scrollArea_table.setObjectName("scrollArea_table")
        self.scrollAreaWidgetContents_table = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_table.setGeometry(QtCore.QRect(0, 0, 1033, 655))
        self.scrollAreaWidgetContents_table.setObjectName(
            "scrollAreaWidgetContents_table"
        )
        self.scrollArea_table.setWidget(self.scrollAreaWidgetContents_table)
        self.verticalLayout.addWidget(self.scrollArea_table)
        self.tabWidget.addTab(self.tab_table, "")
        self.verticalLayout_main.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1079, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionEmail = QtWidgets.QAction(MainWindow)
        self.actionEmail.setObjectName("actionEmail")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionEmail)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UR Force Recorder"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.lineEdit_ip.setText(_translate("MainWindow", "192.168.1.112"))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear"))
        self.label_2.setText(_translate("MainWindow", "Frequency:"))
        self.comboBox_frequency.setItemText(0, _translate("MainWindow", "1 Hz"))
        self.comboBox_frequency.setItemText(1, _translate("MainWindow", "2 Hz"))
        self.comboBox_frequency.setItemText(2, _translate("MainWindow", "5 Hz"))
        self.comboBox_frequency.setItemText(3, _translate("MainWindow", "10 Hz"))
        self.comboBox_frequency.setItemText(4, _translate("MainWindow", "50 Hz"))
        self.comboBox_frequency.setItemText(5, _translate("MainWindow", "100 Hz"))
        self.comboBox_frequency.setItemText(6, _translate("MainWindow", "125 Hz"))
        self.comboBox_frequency.setItemText(7, _translate("MainWindow", "200 Hz"))
        self.comboBox_frequency.setItemText(8, _translate("MainWindow", "300 Hz"))
        self.comboBox_frequency.setItemText(9, _translate("MainWindow", "400 Hz"))
        self.comboBox_frequency.setItemText(10, _translate("MainWindow", "500 Hz"))
        self.checkBox_autoscroll.setText(_translate("MainWindow", "Autoscroll"))
        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_actualFT),
            _translate("MainWindow", "Actual TCP Force/Torque"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_rawFT),
            _translate("MainWindow", "Raw Force/Torque"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_table), _translate("MainWindow", "Table")
        )
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionEmail.setText(
            _translate("MainWindow", "charintorn@autoflexible.com")
        )
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


# import resources_rc


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
