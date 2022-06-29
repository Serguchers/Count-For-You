# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(678, 491)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Main.sizePolicy().hasHeightForWidth())
        Main.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tableTab = QtWidgets.QWidget()
        self.tableTab.setObjectName("tableTab")
        self.gridLayout = QtWidgets.QGridLayout(self.tableTab)
        self.gridLayout.setContentsMargins(0, 2, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.tableTab)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 0, 0)
        self.tabWidget.addTab(self.tableTab, "")
        self.graphTab = QtWidgets.QWidget()
        self.graphTab.setObjectName("graphTab")
        self.tabWidget.addTab(self.graphTab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        Main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 678, 21))
        self.menubar.setObjectName("menubar")
        Main.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(Main)
        self.toolBar.setObjectName("toolBar")
        Main.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # custom code
        Main.setWindowIcon(QtGui.QIcon('icons\main_app_icon.png'))
        self.settings_button = QtWidgets.QAction("Настройки")
        self.toolBar.addAction(self.settings_button)
        self.emailNotSett = QtWidgets.QAction("Email-уведомления")
        self.toolBar.addAction(self.emailNotSett)
        self.tableView.horizontalHeader().setSectionResizeMode(1)
        self.tableView.verticalHeader().setSectionResizeMode(1)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout_1 = QtWidgets.QGridLayout(self.graphTab)
        self.gridLayout_1.setContentsMargins(6, 2, 6, 6)
        self.gridLayout_1.setSpacing(0)
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.retranslateUi(Main)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setDocumentMode(True)
        self.tabWidget.tabBar().setExpanding(True)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "CountForYou"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tableTab), _translate("Main", "Данные")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.graphTab), _translate("Main", "График")
        )
        self.toolBar.setWindowTitle(_translate("Main", "toolBar"))