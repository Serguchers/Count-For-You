import configparser
import os

config = configparser.ConfigParser()
config_path = f"{os.getcwd()}/configurations.ini"
config.read(config_path)
