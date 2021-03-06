from django import dispatch
from telegram.ext import Updater 
from telegram.ext import CommandHandler , CallbackQueryHandler
from telegram.ext import MessageHandler , Filters

#import configparser
from youtube_search import YoutubeSearch
from os import  rename , system , listdir , remove , environ , mkdir 
from subprocess import check_output
from pytube import YouTube , Playlist
from string import punctuation
import logging 
import shutil

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt= '%Y-%m-%d %H:%M')




# get token from config
# config = configparser.ConfigParser()
# config.read('config.ini')
# token = config['TELEGRAM']['ACCESS_TOKEN']

# init bot and setup dispatcher
updater = Updater(token=environ["token"] , use_context=False)
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
    /mp4 url - download video 
    /mp3 url - download audio 
    /list_mp4 url - download video list
    /list_mp3 url - download audio list 
    /search Search - search video
    \
    ''')

# download mp4 command
def mp4(bot , update):
    
    text = update.message['text']
    url = text[10:]
    
    yt = YouTube(url)
   
    #update.message.reply_text(text='Invalid URL!')
        #return 0

    update.message.reply_text(text='downloading...')         
    
    #system(f"youtube-dl {url} --output video.%(ext)s")
    title2 = yt.title.translate(str.maketrans('', '', punctuation))
    if isEnglish(title2) == False:
        title = "video"
    else :
        title = title2    

    yt.streams.get_highest_resolution().download(filename=title+".mp4")    
    #title = "video"
    #for filename in listdir('.'):
    #    if filename.translate(str.maketrans('', '', punctuation)) == title2+'mp4':
    #        rename(filename.replace("mp4","")+'mp4' ,title+".mp4")
    #        break 
    update.message.reply_text(text="Uploading...")
    system(f'curl --upload-file  "{title}.mp4" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
        update.message.reply_text(text = '''
Title : {}
Author : {}
Publish Date : {}
YouTube Url : {} 

Download link : {}
'''.format(yt.title , yt.author , yt.publish_date ,url ,  file.read()))
    remove(title+".mp4")   

# download mp3 command 
def mp3(bot , update):
    
    text = update.message['text']
    url = text[10:]
    
    yt = YouTube(url)
   
    #update.message.reply_text(text='Invalid URL!')
        #return 0

    update.message.reply_text(text='downloading...')         
    


    title2 = yt.title.translate(str.maketrans('', '', punctuation))
    if isEnglish(title2) == False:
        title = "audio"
    else :
        title = title2
    yt.streams.get_audio_only().download(filename=title+".mp3")     
    #title = "video"
    #for filename in listdir('.'):
    #    if filename.translate(str.maketrans('', '', punctuation)) == title2+'mp4':
    #        rename(filename.replace("mp4","")+'mp4' ,title+".mp3")
    #        break 
    update.message.reply_text(text="Uploading...")
    system(f'curl --upload-file  "{title}.mp3" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
                update.message.reply_text(text = '''
Title : {}
Author : {}
Publish Date : {}
YouTube Url : {}

Download link : {}
'''.format(yt.title , yt.author , yt.publish_date ,url ,  file.read()) )
    remove(title+".mp3")

# download mp4 list command 
def list_mp4(bot , update):
    update.message.reply_text(text='downloading...') 
    text = update.message['text']
    url = text[10:]
    p = Playlist(url)
    title = p.title.translate(str.maketrans('', '', punctuation))
    if isEnglish(title) == False:
        title = "video"

    mkdir(title)

    for video in p.videos:
        video.streams.get_highest_resolution().download(title)
        update.message.reply_text(text=f"Downloaded {video.title}")

    update.message.reply_text(text="Zipping...")
    shutil.make_archive(title, 'zip', title)    
    update.message.reply_text(text="Uploading...")
    system(f'curl --upload-file  "{title}.zip" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
        update.message.reply_text(text = '''
Title : {}
Owner : {}
YouTube Url : {}
Download Link :{} 
'''.format(p.title , p.owner , url, file.read()))
    system(f'rd /s /q "{title}"')
    remove(title+".zip")   

# download mp3 list command 
def list_mp3(bot , update):
    update.message.reply_text(text='downloading...') 
    text = update.message['text']
    url = text[10:]
    p = Playlist(url)
    title = p.title.translate(str.maketrans('', '', punctuation))
    if isEnglish(title) == False:
        title = "audio"

    mkdir(title)

    for video in p.videos:
        video.streams.get_audio_only().download(output_path=title , filename="{}.mp3".format(video.title.translate(str.maketrans('', '', punctuation))))
        update.message.reply_text(text=f"Downloaded {video.title}")

    update.message.reply_text(text="Zipping...")
    shutil.make_archive(title, 'zip', title)    
    update.message.reply_text(text="Uploading...")
    system(f'curl --upload-file  "{title}.zip" https://transfer.sh --globoff > link.txt')
    with open("link.txt", "r") as file:
        update.message.reply_text(text = '''
Title : {}
Owner : {}
YouTube Url : {}

Download Link : {}
'''.format(p.title , p.owner , url, file.read()))
    system(f'rd /s /q "{title}"')
    remove(title+".zip")   

def search(bot , update):
    text = update.message['text']
    Search = text.replace("/search" , "")
    results = YoutubeSearch(Search, max_results=5).to_dict()
    update.message.reply_text(text = "Top 5 result of {}".format(Search))
    for result in results:
        update.message.reply_text(text = '''
Title : {}
Url : https://youtube.com{}'''.format(result['title'] , result['url_suffix']))

# error handling
def error (bot,update,error):
    update.message.reply_text(f'''Error : {error}''')

# detmine language of title
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# add handler to dispatcher
dispatcher.add_handler(CommandHandler('start' , start))
dispatcher.add_handler(CommandHandler('mp4' , mp4))
dispatcher.add_handler(CommandHandler('mp3' , mp3))
dispatcher.add_handler(CommandHandler("list_mp4" , list_mp4))
dispatcher.add_handler(CommandHandler("list_mp3" , list_mp3))
dispatcher.add_handler(CommandHandler("search" , search))
dispatcher.add_error_handler(error)

# start running bot
updater.start_polling()
updater.idle()

# stop running bot
updater.stop()