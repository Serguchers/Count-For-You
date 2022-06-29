import os
import sys

sys.path.append(os.getcwd())

import time
import smtplib
from threading import Thread
from log import log_config
from calcs import compare_values
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_notifier.sensetive_data import *
from config import config

log_client = logging.getLogger("client_logger")


class EmailNotifier(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        # Формат данных [(buy_binance, sell_binance), (buy_kucoin, sell_kucoin)]
        self.values_to_compare = []
        # Инициализация сервиса отправки сообщений
        self.server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        self.msg = MIMEMultipart()

    def run(self):
        first_run = True
        message_sent = time.time()
        while True:
            if config["EMAIL_NOTIFICATIONS_SETTINGS"]["enabled"] == "False":
                break
            if first_run:
                try:
                    previous_value_buy = self.values_to_compare[1][0]
                    previous_value_sell = self.values_to_compare[1][1]
                except IndexError:
                    time.sleep(2)
                    continue
                first_run = False
            try:
                margin_buy = compare_values(
                    *self.get_prepared_list(previous_value_buy, "buy")
                )
                margin_sell = compare_values(
                    *self.get_prepared_list(previous_value_sell, "sell")
                )

                if margin_buy > float(
                    config["EMAIL_NOTIFICATIONS_SETTINGS"]["profit_rate"]
                ) or margin_sell > float(
                    config["EMAIL_NOTIFICATIONS_SETTINGS"]["profit_rate"]
                ):
                    # Контроль интервала отправки сообщения, чтоб не было спама
                    if time.time() - message_sent > 210:
                        try:
                            self.send_message(margin_buy, margin_sell)
                        except:
                            log_client.critical("ERROR TRYING SEND MESSAGE")
                            continue
                        else:
                            message_sent = time.time()
            except IndexError:
                time.sleep(2)
                continue
            except Exception as e:
                log_client.critical(f"Произошла ошибка {e}")
                time.sleep(5)
                continue
            else:
                previous_value_buy = self.values_to_compare[1][0]
                previous_value_sell = self.values_to_compare[1][1]
                time.sleep(int(config["SETTINGS"]["request_freq"]) / 1000)

    def get_prepared_list(self, previous_value, operation):
        prepared_list = []
        try:
            if operation == "buy":
                prepared_list = [
                    self.values_to_compare[0][0],
                    self.values_to_compare[1][0],
                    previous_value,
                    operation,
                ]
            else:
                prepared_list = [
                    self.values_to_compare[0][1],
                    self.values_to_compare[1][1],
                    previous_value,
                    operation,
                ]
        except IndexError:
            raise IndexError
        else:
            return prepared_list

    def send_message(self, margin_buy, margin_sell):
        log_client.info(
            f"SENDING MESSAGE binance:{self.values_to_compare[0][0]}, kucoin:{self.values_to_compare[1][0]}, kucoin_sell:{self.values_to_compare[1][1]}"
        )
        message = f"K_b: {self.values_to_compare[1][0]}, K_s: {self.values_to_compare[1][1]}, B: {self.values_to_compare[0][0]} \n P_b: ({margin_buy * 100}%) P_s: ({margin_sell * 100}% \n Актуальная информация."

        password = MY_PASSWORD
        self.msg["From"] = MY_EMAIL
        self.msg["To"] = config["EMAIL_NOTIFICATIONS_SETTINGS"]["target_email"]
        self.msg["Subject"] = "NOTIFICATION FROM APP"

        self.msg.attach(MIMEText(message, "plain"))

        self.server.login(self.msg["From"], password)
        self.server.send_message(self.msg)
        self.server.quit()
