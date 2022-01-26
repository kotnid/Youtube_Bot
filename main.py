from django import dispatch
from telegram.ext import Updater 
from telegram.ext import CommandHandler , CallbackQueryHandler
from telegram.ext import MessageHandler , Filters

import configparser
from os import  rename , system , listdir , remove , environ
from subprocess import check_output
from pytube import YouTube
from string import punctuation
import logging 

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt= '%Y-%m-%d %H:%M')

from importlib_metadata import version


# get token from config
# config = configparser.ConfigParser()
# config.read('config.ini')
# token = config['TELEGRAM']['ACCESS_TOKEN']

# init bot and setup dispatcher
updater = Updater(token="5066041467:AAFtZravwzuEDjKve9VZYiBK_FARNLfnIr0" , use_context=False)
dispatcher = updater.dispatcher

# start command 
def start(bot , update):
    message = update.message
    print(message)
    chat = message['chat']
    update.message.reply_text(text='Hi ' + str(chat['username']))
    update.message.reply_text(text='''\
    The usage of this bot is download video from Youtube

The source code of the bot is available at https://github.com/kotnid/Youtube_Bot
Command available : 
    /start - show this message
    /download url - download video (warning : only English title functionable now!!)
    \
    ''')

# download command
def download(bot , update):
    
    text = update.message['text']
    url = text[10:]
    
    #yt = YouTube(url)
   
    #update.message.reply_text(text='Invalid URL!')
        #return 0

    update.message.reply_text(text='downloading...')         
    #yt.streams.get_highest_resolution().download()
    system(f"youtube-dl {url} --output %(title)s.%(ext)s")
    #title = yt.title.translate(str.maketrans('', '', punctuation))
    title = "video"
    #for filename in listdir('.'):
    #    if filename.translate(str.maketrans('', '', punctuation)) == title+'mp4':
    #        rename(filename.replace("mp4","")+'mp4' ,title+".mp4")
    #        break 

    system(f'curl --upload-file  "{title}.mp4" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
        update.message.reply_text(text = "Download your video here : {}".format(file.read()))
    remove(title+".mp4")   

# error handling
def error (bot,update,error):
    update.message.reply_text(f'''error : {error}''')

def test(bot , update):
    update.message.reply_text(text = version("pytube"))

# add handler to dispatcher
dispatcher.add_handler(CommandHandler('start' , start))
dispatcher.add_handler(CommandHandler('download' , download))
dispatcher.add_handler(CommandHandler('test' , test))
#dispatcher.add_error_handler(error)
# start running bot
updater.start_polling()
updater.idle()

# stop running bot
updater.stop()