import asyncio
import aiohttp
import sys
import os
import configparser
from headers import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QHeaderView
from client_interface import MainWindow, ConfigWindow
from config import config


app = QApplication(sys.argv)
main_window = MainWindow()
stylesheetFile = f'interface\stylesheets\{config["SETTINGS"]["app_style"]}.qss'
with open(stylesheetFile, "r") as st:
    app.setStyleSheet(st.read())
sys.exit(app.exec_())
