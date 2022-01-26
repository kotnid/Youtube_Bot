from telegram.ext import Updater 
from telegram.ext import CommandHandler , CallbackQueryHandler
from telegram.ext import MessageHandler , Filters

import configparser

# get token from config
config = configparser.ConfigParser()
config.read('config.ini')
token = config['TELEGRAM']['ACCESS_TOKEN']
