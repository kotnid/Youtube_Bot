from django import dispatch
from telegram.ext import Updater 
from telegram.ext import CommandHandler , CallbackQueryHandler
from telegram.ext import MessageHandler , Filters

import configparser
from os import  rename , system , listdir , remove , environ
from subprocess import check_output
from pytube import YouTube
from string import punctuation

# get token from config
# config = configparser.ConfigParser()
# config.read('config.ini')
# token = config['TELEGRAM']['ACCESS_TOKEN']

# init bot and setup dispatcher
updater = Updater(token=environ['token'] , use_context=False)
dispatcher = updater.dispatcher

# start command 
def start(bot , update):
    message = update.message
    print(message)
    chat = message['chat']
    update.message.reply_text(text='Hi ' + str(chat['username']))
    update.message.reply_text(text='''\
    The usage of this bot is download video from Youtube
This bot 
Command available : 
    /start - show this message
    \
    ''')

# download command
def download(bot , update):
    
    text = update.message['text']
    url = text[10:]
    try:
        yt = YouTube(url)
    except:
        update.message.reply_text(text='Invalid URL!')
        return 0

    update.message.reply_text(text='downloading...')         
    yt.streams.get_highest_resolution().download()
    title = yt.title.translate(str.maketrans('', '', punctuation))
    for filename in listdir('.'):
        if filename.translate(str.maketrans('', '', punctuation)) == title+'mp4':
            rename(filename.replace("mp4","")+'mp4' ,title+".mp4")
            break 

    system(f'curl --upload-file  "{title}.mp4" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
        update.message.reply_text(text = "Download your video here : {}".format(file.read()))
    remove(title+".mp4")   

# add handler to dispatcher
dispatcher.add_handler(CommandHandler('start' , start))
dispatcher.add_handler(CommandHandler('download' , download))

# start running bot
updater.start_polling()
updater.idle()

# stop running bot
updater.stop()