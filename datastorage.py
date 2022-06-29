import datetime
import os
import sys
import sqlite3
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker


class FinanceData:
    class Binance_data:
        def __init__(self, price):
            self.id = None
            self.price = price
            self.date = datetime.datetime.now()

    def __init__(self):
        self.database_engine = sqlalchemy.create_engine(
            f"sqlite:///financial_data",
            echo=False,
            connect_args={"check_same_thread": False},
        )

        self.metadata = sqlalchemy.MetaData()

        binance_table = sqlalchemy.Table(
            "binance",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("price", sqlalchemy.Float),
            sqlalchemy.Column("date", sqlalchemy.DateTime),
        )

        self.metadata.create_all(self.database_engine)

        mapper(self.Binance_data, binance_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

    def write_data(self, price):
        new_data = self.Binance_data(price)
        self.session.add(new_data)
        self.session.commit()

    def select_last(self, session_time):
        data = (
            self.session.query(self.Binance_data.price, self.Binance_data.date)
            .where(self.Binance_data.date >= session_time)
            .order_by(self.Binance_data.date.desc())
            .limit(2)
        )
        self.session.commit()
        return data
