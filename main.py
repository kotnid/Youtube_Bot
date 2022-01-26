from django import dispatch
from telegram.ext import Updater 
from telegram.ext import CommandHandler , CallbackQueryHandler
from telegram.ext import MessageHandler , Filters

import configparser

# get token from config
config = configparser.ConfigParser()
config.read('config.ini')
token = config['TELEGRAM']['ACCESS_TOKEN']

# init bot and setup dispatcher
updater = Updater(token=token , use_context=False)
dispatcher = updater.dispatcher

# start command 
def start(bot , update):
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='Hi ' + str(chat['username']))
    update.message.reply_text(text='''\
    The usage of this bot is download video from Youtube
    Command available : 
    /start - show this message
    \
    ''')

# add handler to dispatcher
dispatcher.add_handler(CommandHandler('start' , start))

# start running bot
updater.start_polling()
updater.idle()

# stop running bot
updater.stop()