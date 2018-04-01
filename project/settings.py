import os
from configparser import ConfigParser

config = ConfigParser()

PROJECT_NAME = 'squeezer'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

prod_config_path = os.path.join(f'/etc/{PROJECT_NAME}/{PROJECT_NAME}.conf')
local_config_path = os.path.join(BASE_DIR, 'build', 'conf', 'local.conf')

config_path = prod_config_path if os.path.exists(prod_config_path) else local_config_path
config.read(config_path)

HOST = config.get('main', 'HOST')
PORT = config.getint('main', 'PORT')

TELEGRAM_BOT_TOKEN = config.get('telegram', 'BOT_TOKEN')
