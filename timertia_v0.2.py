import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random
import datetime
import time
from cryptography.fernet import Fernet
import os
from calculator.simple import SimpleCalculator
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

key = Fernet.generate_key()
fernet = Fernet(key)

characters = open('chars.txt', 'a', encoding="utf-8")
players = open('players.txt', 'a', encoding='utf-8')
admin = open('admin.txt', encoding="utf-8").read().splitlines()
rnd_word = open('random_word.txt', encoding="utf-8").read()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def familynamegenerator():
    glasny = 120*["e"]+81*["a"]+77*["o"]+73*["i"]+29*["u"]+21*["y"]
    soglasny = 91*["t"]+70*["n"]+63*["s"]+60*["r"]+59*["h"]+43*["d"]+40*["l"]+27*["c"]+26*["m"]+23*["f"]+21*["w"]+20*["g"]+18*["p"]+15*["b"]+11*["v"]+7*["k"]+2*["x"]+1*["q"]+1*["j"]+1*["z"]
    slovar = ""
    first = ''
    second = ''
    letternumber = random.randint(3,10)
    pervoglas = 0
    coin = random.randint(0,1)

    if coin == 1:
        first = glasny[random.randint(0,len(glasny)-1)]
        first = first.upper()
        pervoglas = 1
    else:
        first = soglasny[random.randint(0,len(soglasny)-20)]
        first = first.upper()

    for i in range(letternumber-1):  
        if pervoglas == 0:
            coin = random.randint(1,10)
            if coin == 1:
                second += soglasny[random.randint(0,len(soglasny)-1)]
                pervoglas = 0
            else:
                second += glasny[random.randint(0,len(glasny)-1)]
                pervoglas = 1      
        else:
            coin = random.randint(1,10)
            if coin == 1:
                second += glasny[random.randint(0,len(glasny)-1)]
                pervoglas = 1
            else:
                second += soglasny[random.randint(0,len(soglasny)-20)]
                pervoglas = 0

    slovar += first + second

    return slovar

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Меня зовут Тимертия, господин " + str(update.effective_user.first_name) + "!\nЯ бот-служанка, буду рада помочь.")
    
async def mychar(update, context):
    name = update.effective_user.first_name
    surname = update.effective_user.last_name
    code = update.effective_user.id
    stats = str(update.effective_message.text)
    stats = [int(s) for s in stats.split() if s.isdigit()]
    if sum(stats) <= 10 and stats != []:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(name) + " " + str(surname) + " " + str(code) + "\nВаши статы:" + "\nСила:" + str(stats[0]) + "\nЛовкость:" + str(stats[1]) + "\nИнтеллект:" + str(stats[2])))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ОШИБКА! Введите статы суммой не больше 10!")

async def shifr(update, context):
    message = str(update.effective_message.text)
    message = message.replace("/shifr ","")
    encMessage = fernet.encrypt(message.encode())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=encMessage.decode())
   
async def deshifr(update, context):
    message = str(update.effective_message.text)
    if admin[1] in message:
        message = message.replace("/deshifr ","")
        message = message.replace(admin[1] + " ","")
        decMessage = fernet.decrypt(message.encode())
        await context.bot.send_message(chat_id=update.effective_chat.id, text=decMessage.decode())
    elif str(update.effective_user.id) == admin[0]:
        message = message.replace("/deshifr ","")
        decMessage = fernet.decrypt(message.encode())
        await context.bot.send_message(chat_id=update.effective_chat.id, text=decMessage.decode()) 
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")

async def setpass(update, context):
    global admin
    admin_id = admin[0]
    if str(update.effective_user.id) == admin_id:
        message = str(update.effective_message.text)
        message = message.replace("/setpass ","")
        admin[1] = message
        bufer = open('admin.txt', 'w',encoding="utf-8")
        bufer.write(admin[0] + "\n" + admin[1])
        bufer.close()
        admin = open('admin.txt', encoding="utf-8").read().splitlines()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", новый пароль:\n" + message))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Тебе не дозволено устанаваливать пароли, холоп, знай своё место!")
            
async def hentai(update, context):
    message = str(update.effective_message.text)
    manga = random.randint(2,402560)
    page = random.randint(1,10)
    req = Request(url = "https://nhentai.to/g/" + str(manga) + "/" + str(page) + "/", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            continue
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content) 
    pattern = "[\=,\(][\"|\'].[^\=\"]+\.(?i:jpg|gif|png|bmp)[\"|\']"
    if admin[1] in message:
        if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
            await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga))
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga))
    elif str(update.effective_user.id) == admin[0]:
        if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
            await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga))
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")
    if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.jpg')
    elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.png')    
          
async def calculate(update, context):
        message = str(update.effective_message.text)
        message = message.replace("/calculate ","")
        answer = SimpleCalculator()
        answer.run(message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer.lcd)
        
async def maze(update, context):
    message = str(update.effective_message.text)
    if admin[1] in message:
        os.system("mazegen.py 1")
        await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\maze10.png', 'rb'))
    else:
        os.system("mazegen1.py 1")
        await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\maze.png', 'rb'))
    
async def random_command(update, context):
    global rnd_word
    rnd_word = familynamegenerator()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="А теперь новая команда: " + rnd_word)
    new_word = open('random_word.txt', 'w',encoding="utf-8")
    new_word.write(rnd_word)
    new_word.close()
    rnd_word = open('random_word.txt', encoding="utf-8").read().rstrip()
    random_command_handler = CommandHandler(rnd_word, random_command)
      
if __name__ == '__main__':
    
    application = ApplicationBuilder().token("TOKEN").build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.add_handler(CommandHandler('mychar', mychar))
    
    application.add_handler(CommandHandler('shifr', shifr))
    
    application.add_handler(CommandHandler('deshifr', deshifr))
    
    application.add_handler(CommandHandler('setpass', setpass))
    
    application.add_handler(CommandHandler('hentai', hentai))
    
    application.add_handler(CommandHandler('calculate', calculate))
    
    application.add_handler(CommandHandler('maze', maze))
    
    application.add_handler(CommandHandler(rnd_word, random_command))
   
    application.run_polling()