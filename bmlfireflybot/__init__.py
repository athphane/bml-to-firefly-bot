import ast
from configparser import ConfigParser
from bmlfireflybot.bmlfireflybot import BmlFireflyBot

BmlFireflyBot = BmlFireflyBot(__name__)

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

# Get from config file.
ADMINS = ast.literal_eval(config.get('bot', 'admins'))

MONGO_URL = config.get('mongo', 'url')
DB_NAME = config.get('mongo', 'db_name')
DB_USERNAME = config.get('mongo', 'db_username')
DB_PASSWORD = config.get('mongo', 'db_password')

client = None
