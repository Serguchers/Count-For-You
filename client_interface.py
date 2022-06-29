import asyncio
import configparser
import os
import datetime

from interface.main_window import Ui_Main
from interface.settings_window import Ui_Settings
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from main import USDT_RUB_PAIR, main
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal
from calcs import find_best_offer
from win10toast import ToastNotifier
from log import log_config
import logging
from config import config
from datastorage import FinanceData
from email_notifier.email_notifier import EmailNotifier
from interface.email_not_sett import Ui_EmailSettings


windows_notifier = ToastNotifier()
log_client = logging.getLogger("client_logger")
datastorage = FinanceData()
email_notifier = EmailNotifier()


SELECTED_RESOURCES = USDT_RUB_PAIR.keys()
AVAILABLE_STYLES = ["Aqua", "Dark", "MacOs", "Forbidden"]


class QStandardItemExt(QStandardItem):
    def __init__(self, item):
        super().__init__(item)
        self.setEditable(False)
        self.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.custom_font = QFont()

    def highlight(self):
        self.setForeground(QColor("green"))
        self.custom_font.setBold(True)
        self.setFont(self.custom_font)


class CustomPlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__(axisItems={"bottom": pg.DateAxisItem()})
        self.session_time = datetime.datetime.now()
        self.plotItem.setMouseEnabled(x=False)
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setTitle("Binance")
        self.set_background()

    def build_plot(self):
        recent_data = datastorage.select_last(self.session_time)
        self.plot(
            [x[1].timestamp() for x in recent_data],
            [x[0] for x in recent_data],
            pen=self.pen,
        )

    def set_background(self):
        if config["SETTINGS"]["app_style"] == "Dark":
            self.pen = pg.mkPen(color=(255, 255, 255))
            super().setBackground("black")
        else:
            self.pen = pg.mkPen(color=(46, 36, 240))
            super().setBackground("w")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.ui.settings_button.triggered.connect(self.show_settings)
        self.ui.emailNotSett.triggered.connect(self.show_email_not_settings)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visual_data)
        self.timer.start(int(config["SETTINGS"]["request_freq"]))

        self.graphWidget = CustomPlotWidget()
        self.ui.gridLayout_1.addWidget(self.graphWidget, 0, 0, 1, 1)

        self.previous_best_buy = None
        self.previous_best_sell = None

        if config["EMAIL_NOTIFICATIONS_SETTINGS"]["enabled"] == "True":
            email_notifier.start()

        self.update_visual_data()
        self.show()

    def fill_table(self):
        # Функция обновления таблицы
        USDT_RUB_PAIR = MainWindow.get_fresh_data()
        MainWindow.write_log()
        email_notifier.values_to_compare = [
            (USDT_RUB_PAIR["binance"]["buy"], USDT_RUB_PAIR["binance"]["sell"]),
            (USDT_RUB_PAIR["kucoin"]["buy"], USDT_RUB_PAIR["kucoin"]["sell"]),
        ]

        table_row = QStandardItemModel()
        table_row.setHorizontalHeaderLabels(["Ресурс", "Цена", "Цена"])
        best_buy, best_sell = find_best_offer(
            {resource: USDT_RUB_PAIR[resource] for resource in SELECTED_RESOURCES}
        )

        for resource in SELECTED_RESOURCES:
            price_buy = QStandardItemExt(
                "{:10.2f}".format(USDT_RUB_PAIR[resource]["buy"])
            )
            price_sell = QStandardItemExt(
                "{:10.2f}".format(USDT_RUB_PAIR[resource]["sell"])
            )
            if resource is best_buy:
                # Проверяем сменился ли лидер
                if (
                    self.previous_best_buy is not None
                    and self.previous_best_buy != resource
                ):
                    MainWindow.show_win_not(f"Новый лучший оффер на покупку {resource}")
                self.previous_best_buy = resource
                price_buy.highlight()

            elif resource is best_sell:
                # Проверяем сменился ли лидер
                if (
                    self.previous_best_sell is not None
                    and self.previous_best_sell != resource
                ):
                    MainWindow.show_win_not(f"Новый лучший оффер на продажу {resource}")
                self.previous_best_sell = resource
                price_sell.highlight()

            resource = QStandardItemExt(resource.capitalize())
            table_row.appendRow([resource, price_buy, price_sell])

        self.ui.tableView.setModel(table_row)

    @staticmethod
    def get_fresh_data():
        # Получение up-to-date данных
        USDT_RUB_PAIR = asyncio.get_event_loop().run_until_complete(
            main(SELECTED_RESOURCES)
        )
        datastorage.write_data(USDT_RUB_PAIR["binance"]["buy"])
        return USDT_RUB_PAIR

    def show_settings(self):
        # Показать настройки
        self.config_window = ConfigWindow()
        self.config_window.settings_changed.connect(self.new_timer_interval)

    def show_email_not_settings(self):
        # Показать настройки email-уведомлений
        self.email_not_settings = EmailNotificationsConfig()

    @pyqtSlot(int)
    def new_timer_interval(self, new_interval):
        # Слот для обработки сигнала о смене временного интервала запросов
        self.update_visual_data()
        self.timer.stop()
        self.timer.start(new_interval)

    def update_visual_data(self):
        # Последовательность обновления данных
        self.fill_table()
        self.graphWidget.build_plot()

    @staticmethod
    def write_log():
        if config["SETTINGS"]["logging"] == "True":
            log_client.info(USDT_RUB_PAIR)

    @staticmethod
    def show_win_not(text):
        if config["SETTINGS"]["windows_notifications"] == "True":
            windows_notifier.show_toast(title='Новый выгодный оффер!', msg=text, icon_path='icons\win_not.ico', threaded=True)


class ConfigWindow(QtWidgets.QWidget):
    settings_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        # Заполнение частоты запросов
        self.ui.settReqFreq.setValue(int(config["SETTINGS"]["request_freq"]) / 1000)
        self.ui.settReqFreq.setMinimum(5)
        # Заполнение выбора опции логирования
        if config["SETTINGS"]["logging"] == "True":
            self.ui.loggingCheck.setChecked(True)
        # Заполнения выбора опции уведомлений
        if config["SETTINGS"]["windows_notifications"] == "True":
            self.ui.WinNotSett.setChecked(True)
        # Заполнение выбранных источников, при запуске показываются все доступные
        for resource in USDT_RUB_PAIR.keys():
            self.ui.resourceSett.addItem(resource)
        # Заполнение combo-box доступными стилями
        for style in AVAILABLE_STYLES:
            self.ui.styleSett.addItem(style)
        self.ui.styleSett.setCurrentText(config["SETTINGS"]["app_style"])
        # Заполнение phemex-токена
        self.ui.phemexAuthTok.setText(config["SETTINGS"]["phemex_auth_token"])

        self.show()

        self.ui.saveButton.clicked.connect(self.saveSettings)
        self.ui.exitButton.clicked.connect(self.close)

    def saveSettings(self):
        # Сохранить настройки
        global SELECTED_RESOURCES
        if len(self.ui.resourceSett.selectedItems()) != 0:
            SELECTED_RESOURCES = [
                selected_item.text()
                for selected_item in self.ui.resourceSett.selectedItems()
            ]

        if config["SETTINGS"]["request_freq"] != str(
            self.ui.settReqFreq.value() * 1000
        ):
            config["SETTINGS"]["request_freq"] = str(self.ui.settReqFreq.value() * 1000)
            self.settings_changed.emit(self.ui.settReqFreq.value() * 1000)
        config["SETTINGS"]["logging"] = str(self.ui.loggingCheck.isChecked())
        config["SETTINGS"]["app_style"] = self.ui.styleSett.currentText()
        config["SETTINGS"]["windows_notifications"] = str(
            self.ui.WinNotSett.isChecked()
        )
        config["SETTINGS"]["phemex_auth_token"] = str(self.ui.phemexAuthTok.text())

        with open("configurations.ini", "w") as conf:
            config.write(conf)


class EmailNotificationsConfig(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EmailSettings()
        self.ui.setupUi(self)

        if config["EMAIL_NOTIFICATIONS_SETTINGS"]["enabled"] == "True":
            self.ui.emailOnSet.setChecked(True)

        self.ui.userEmailSet.setText(
            config["EMAIL_NOTIFICATIONS_SETTINGS"]["target_email"]
        )
        self.ui.profitRateSet.setValue(
            float(
                config["EMAIL_NOTIFICATIONS_SETTINGS"]["profit_rate"].replace(",", ".")
            )
        )

        self.ui.saveBut.clicked.connect(self.saveSettings)
        self.ui.exitBut.clicked.connect(self.close)
        self.show()

    def saveSettings(self):
        previous_state = config["EMAIL_NOTIFICATIONS_SETTINGS"]["enabled"]
        config["EMAIL_NOTIFICATIONS_SETTINGS"]["enabled"] = str(
            self.ui.emailOnSet.isChecked()
        )
        config["EMAIL_NOTIFICATIONS_SETTINGS"][
            "target_email"
        ] = self.ui.userEmailSet.text()
        config["EMAIL_NOTIFICATIONS_SETTINGS"]["profit_rate"] = str(
            self.ui.profitRateSet.value()
        )

        with open("configurations.ini", "w") as conf:
            config.write(conf)

        if previous_state == "False" and self.ui.emailOnSet.isChecked():
            global email_notifier
            email_notifier = EmailNotifier()
            email_notifier.start()
