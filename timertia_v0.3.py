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
from telegram.error import BadRequest
import html

messages = []

key = Fernet.generate_key()
fernet = Fernet(key)

keys = open('keys.txt', 'a', encoding="utf-8")
keys.write("\n" + str(datetime.datetime.now())+ " КЛЮЧ: " + str(key))
keys.close()  

    # Open the file in read mode
characters = open('chars.txt', 'a', encoding="utf-8")
log = open('log.txt', 'a', encoding="utf-8")
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
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text="Меня зовут Тимертия, господин " + str(update.effective_user.first_name) + "!\nЯ бот-служанка, буду рада помочь (/help).")
    messages.append(y.message_id)
    #time.sleep(10)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Пока!")
    log.write("\n" + str(datetime.datetime.now()) +" /start " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    
async def mychar(update, context):
    name = update.effective_user.first_name
    surname = update.effective_user.last_name
    code = update.effective_user.id
    stats = str(update.effective_message.text)
    log.write(str(datetime.datetime.now()) + stats)
    stats = [int(s) for s in stats.split() if s.isdigit()]
    if sum(stats) <= 10 and stats != []:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(name) + " " + str(surname) + " " + str(code) + "\nВаши статы:" + "\nСила:" + str(stats[0]) + "\nЛовкость:" + str(stats[1]) + "\nИнтеллект:" + str(stats[2])))
        messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="ОШИБКА! Введите статы суммой не больше 10!")
        messages.append(y.message_id)

async def shifr(update, context):
    message = str(update.effective_message.text)
    message = message.replace("/shifr ","")
    encMessage = fernet.encrypt(message.encode())
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=encMessage.decode())
    messages.append(y.message_id)
    log.write("\n" + str(datetime.datetime.now()) +" /shifr " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
   
async def deshifr(update, context):
    message = str(update.effective_message.text)
    log.write("\n" + str(datetime.datetime.now()) +" /deshifr " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    if admin[1] in message:
        message = message.replace("/deshifr ","")
        message = message.replace(admin[1] + " ","")
        decMessage = fernet.decrypt(message.encode())
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=decMessage.decode())
        messages.append(y.message_id)
    elif str(update.effective_user.id) == admin[0] or str(update.effective_user.id) == admin[2] or str(update.effective_user.id) == admin[3] or str(update.effective_user.id) == admin[4]:
        message = message.replace("/deshifr ","")
        decMessage = fernet.decrypt(message.encode())
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=decMessage.decode()) 
        messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")
        messages.append(y.message_id)

async def setpass(update, context):
    global admin
    admin_id = admin[0]
    log.write("\n" + str(datetime.datetime.now()) +" /setpass " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    if str(update.effective_user.id) == admin_id:
        message = str(update.effective_message.text)
        message = message.replace("/setpass ","")
        admin[1] = message
        bufer = open('admin.txt', 'w',encoding="utf-8")
        bufer.write(admin[0] + "\n" + admin[1]  + "\n" + admin[2] + "\n" + admin[3] + "\n" + admin[4])
        bufer.close()
        admin = open('admin.txt', encoding="utf-8").read().splitlines()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", новый пароль:\n" + message))
        messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="Тебе не дозволено устанаваливать пароли, холоп, знай своё место!")
        messages.append(y.message_id)
        
async def hesoyam(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /hesoyam " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    message = str(update.effective_message.text)
    if admin[1] in message:
        message = message.replace(admin[1],"")
        stats = [int(s) for s in message.split() if s.isdigit()]
        players = open('players.txt', 'r', encoding="utf-8")
        players_list1 = players.read().splitlines()
        players.close()
        for j in range(len(players_list1)):
            if str(update.effective_user.id) == players_list1[j]:
                players_list1[j+1] = str(stats[0]+250000)
                players = open('players.txt', 'w', encoding="utf-8")
                longlist = ""
                for l in range(len(players_list1)):
                    longlist += (players_list1[l]+"\n")
                players.write(longlist)
                players.close()  
                break
            else:
                None
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="Cheat Activated:" + "\nHesoyam.")
        messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")
        messages.append(y.message_id)
                     
async def hentai(update, context):
    message = str(update.effective_message.text)
    log.write("\n" + str(datetime.datetime.now()) +" /hentai " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    manga = random.randint(2,402560)
    page = 1
    url = "https://nhentai.to/g/" + str(manga) + "/" + str(page) + "/"
    while True:
        if requests.head(url, allow_redirects=True).status_code == 200:
            break
        else:
            url = "https://nhentai.to/g/" + str(random.randint(2,402560)) + "/" + str(page) + "/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    elif str(update.effective_user.id) == admin[0] or str(update.effective_user.id) == admin[2] or str(update.effective_user.id) == admin[3] or str(update.effective_user.id) == admin[4]:
        if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")
        messages.append(y.message_id)
    if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.jpg')
    elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.png') 
    page = random.randint(2,10)
    url = "https://nhentai.to/g/" + str(manga) + "/" + str(page) + "/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    elif str(update.effective_user.id) == admin[0] or str(update.effective_user.id) == admin[2] or str(update.effective_user.id) == admin[3] or str(update.effective_user.id) == admin[4]:
        if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    else:
        None
    if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.jpg')
    elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.png')    
    page = random.randint(11,20)
    url = "https://nhentai.to/g/" + str(manga) + "/" + str(page) + "/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    elif str(update.effective_user.id) == admin[0] or str(update.effective_user.id) == admin[2] or str(update.effective_user.id) == admin[3] or str(update.effective_user.id) == admin[4]:
        if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.jpg', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
        elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\\' + str(page) + '.png', 'rb'), caption=str(manga) + "\n" + "https://nhentai.to/g/" + str(manga) + "/" + "\n/hentai")
            messages.append(y.message_id)
    else:
        None
    if os.path.isfile('G:\Timertia_bot\\' + str(page) + '.jpg') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.jpg')
    elif os.path.isfile('G:\Timertia_bot\\' + str(page) + '.png') == True:
        os.remove('G:\Timertia_bot\\' + str(page) + '.png')        
          
async def calc(update, context):
        log.write("\n" + str(datetime.datetime.now()) +" /calc " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
        message = str(update.effective_message.text)
        message = message.replace("/calc ","")
        answer = SimpleCalculator()
        answer.run(message)
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=answer.lcd)
        messages.append(y.message_id)
        
async def random_num(update, context):
        log.write("\n" + str(datetime.datetime.now()) +" /random_num " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
        message = str(update.effective_message.text)
        message = message.replace("/ranum ","")
        if message != "/ranum":
            answer = random.randint(0,int(message))
        else:
            answer = random.randint(0,100)
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=str(answer))
        messages.append(y.message_id)
   
async def news(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /news " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    date0 = datetime.datetime.strptime("02/23/2022", '%m/%d/%Y')
    date1 = datetime.datetime.today()
    days = date1 - date0
    days = str(days).split(' days')[0]
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text= str(datetime.date.today()) + ". Сегодня идёт " + days + "-ый день войны на Украине.")
    messages.append(y.message_id)
   
async def maze(update, context):
    message = str(update.effective_message.text)
    log.write("\n" + str(datetime.datetime.now()) +" /maze " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    if admin[1] in message:
        os.system("mazegen.py 1")
        y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\maze10.png', 'rb'))
        messages.append(y.message_id)
    else:
        os.system("mazegen1.py 1")
        y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\maze.png', 'rb'))
        messages.append(y.message_id)
    
async def random_command(update, context):
    rnd_word = familynamegenerator()
    log.write("\n" + str(datetime.datetime.now()) +" /random_command " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id) + " новая команда: " + rnd_word)
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=rnd_word)
    messages.append(y.message_id)
    
async def ruletka(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /blackjack " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    players = open('players.txt', 'r', encoding="utf-8")
    players_list = players.read().splitlines()
    players.close()
    stavka = [int(s) for s in str(update.effective_message.text).split() if s.isdigit()]
    found = 0
    for k in range(len(players_list)):
        if str(update.effective_user.id) == players_list[k]:
            found = 1
            #time.sleep(2)
            #await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1]))
            time.sleep(2)
            money = int(players_list[k+1])
            w = random.randint(0,36)
            rb = random.randint(0,1)
            if money >= stavka[1]:
                if w == stavka[0]:
                    money += stavka[1]*35
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", выпало: " + str(w) + "\nВы выиграли: " + str(stavka[1]*35) + ".\nТеперь у вас: " + str(money)))
                    messages.append(y.message_id)
                elif stavka[0] == 100 and w%2 == 0 and w != 0:
                    money += stavka[1]
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) +  ", выпало: " + str(w) + "\nВы выиграли: " + str(stavka[1]) + ".\nТеперь у вас: " + str(money)))
                    messages.append(y.message_id)
                elif stavka[0] == 100 and w%2 == 1 and w != 0:
                    money -= stavka[1]
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) +  ", выпало: " + str(w) + "\nТеперь у вас: " + str(money)))
                    messages.append(y.message_id)
                elif stavka[0] == 101 and w%2 == 1 and w != 0:
                    money += stavka[1]
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) +  ", выпало: " + str(w) + "\nВы выиграли: " + str(stavka[1]) + ".\nТеперь у вас: " + str(money)))
                    messages.append(y.message_id)
                elif stavka[0] == 101 and w%2 == 0 and w != 0:
                    money -= stavka[1]
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) +  ", выпало: " + str(w) + "\nТеперь у вас: " + str(money)))
                    messages.append(y.message_id)
                else:
                    money -= stavka[1]
                    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", выпало: " + str(w) + "\nТеперь у вас: " + str(money)))   
                    messages.append(y.message_id)
            else:
                y = await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя не хватает денег, холоп!")           
                messages.append(y.message_id)
            players = open('players.txt', 'r', encoding="utf-8")
            players_list1 = players.read().splitlines()
            players.close()
            for j in range(len(players_list1)):
                if str(update.effective_user.id) == players_list1[j]:
                    players_list1[j+1] = str(money)
                    players = open('players.txt', 'w', encoding="utf-8")
                    longlist = ""
                    for l in range(len(players_list1)):
                        longlist += (players_list1[l]+"\n")
                    players.write(longlist)
                    players.close()  
                    break
                else:
                    None
            break
    if found == 0:
        players = open('players.txt', 'a', encoding="utf-8")
        players.write(str(update.effective_user.id) + "\n" + str(1000) + "\n")
        players.close()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + str(1000)))
        messages.append(y.message_id)
        
async def capital(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /capital " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    players = open('players.txt', 'r', encoding="utf-8")
    players_list = players.read().splitlines()
    players.close()
    found = 0
    for k in range(len(players_list)):
        if str(update.effective_user.id) == players_list[k]:
            found = 1
            money = players_list[k+1]
            moneys = open('money_buffer.txt', 'w', encoding="utf-8")
            moneys.write(money)
            moneys.close()
            os.system("capital.py 1")
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\gold.png', 'rb'), caption="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + money)
            messages.append(y.message_id) 
            break
    if found == 0:
        players = open('players.txt', 'a', encoding="utf-8")
        players.write(str(update.effective_user.id) + "\n" + str(1000) + "\n")
        players.close()
        moneys = open('money_buffer.txt', 'w', encoding="utf-8")
        moneys.write("1000")
        moneys.close()
        os.system("capital.py 1")
        y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\gold.png', 'rb'), caption="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + "1000")
        messages.append(y.message_id)
                 
async def badapple(update, context):
    message = str(update.effective_message.text)
    log.write("\n" + str(datetime.datetime.now()) +" /FLOOD " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    i = 0
    y = await context.bot.send_audio(update.effective_chat.id, audio=open('G:\Timertia_bot\mapple.mp3', 'rb'))
    messages.append(y.message_id)
    if str(update.effective_user.id) == admin[0]:
        #frames = os.listdir('G:\Timertia_bot\mapple')
        while i < 6470:
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\mapple\\' + 'bad_apple_' + str(40+i) + ".png", 'rb'))
            messages.append(y.message_id)
            time.sleep(3)
            i += 10        
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text="У тебя нет доступа, холоп!")
        messages.append(y.message_id)
        
async def rumors(update, context):
    message = str(update.effective_message.text)
    message = message.replace("/rumors@timertia_bot ","")
    message = message.replace("/rumors ","")
    message = message.replace("/rumors@timertia_bot","")
    message = message.replace("/rumors","")
    if message != "":
        rum = open('mrumors.txt', 'a', encoding="utf-8")
        rum.write("\n" + message)
        rum.close()
    else:
        lines = open('mrumors.txt', encoding="utf-8").read().splitlines()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(lines))
        messages.append(y.message_id)
        
async def bible(update, context):
    bibly = open('Bibold.txt', 'r',  encoding="utf-8")
    bible_lines = bibly.read().splitlines()
    bibly.close()
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(bible_lines))
    messages.append(y.message_id)
    log.write("\n" + str(datetime.datetime.now()) + " /bible " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    
async def rumors_all(update, context):
    y = await context.bot.send_document(chat_id=update.effective_chat.id, document=open('G:\Timertia_bot\mrumors.txt', 'rb'), filename="rumors.txt")
    messages.append(y.message_id)
      
async def help_1(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /help " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Я к вашим услугам, господин, " + str(update.effective_user.first_name)
    + ".\n/shifr <b>текст</b> - шифрую сообщение" 
    + ".\n/deshifr <b>пароль шифр</b> - расшифровываю любой шифр, созданный мной" 
    + ".\n/maze - рисую лабиринт (с паролем другой алгоритм)" 
    + ".\n/calc <b>число операция число</b> - умею +,-,*,/ рациональные числа" 
    + ".\n/ranum <b>число</b> - пишу случайное целое число в заданном интервале" 
    + ".\n/ranword - пишу случайное слово" 
    + ".\n/ruletka <b>число ставка</b> - кручу рулетку (100 на чёт, 101 на нечёт)" 
    + ".\n/hesoyam <b>пароль число</b> - даю денег" 
    + ".\n/capital - показываю ваш капитал" 
    + ".\n/news - сообщаю свежие новости" 
    + ".\n/badapple <b>пароль</b> - дудошу чат аниме" 
    + ".\n<tg-spoiler>/hentai  <b>пароль</b> - показываю кое-что</tg-spoiler>" 
    + ".\n/rumors - рассказываю анонимные слухи (если ввести сообщение, то добавлю его к слухам)" 
    + ".\n/rumors_all - высылаю txt со всеми слухами"
    + ".\n/bible - цитирую Библию" 
    + ".\n/clean <b>пароль</b> - убираю за собой."
    ), parse_mode="HTML")
    messages.append(y.message_id)
   
async def clean(update, context):
    global messages
    buffer = []
    message = str(update.effective_message.text)
    log.write("\n" + str(datetime.datetime.now()) +" /clean " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    if admin[1] in message:
        for i in range(len(messages)):
            try:
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messages[i])
            except (BadRequest, NameError, ValueError):
                buffer.append(messages[i])
                continue
        messages = buffer
   
if __name__ == '__main__':
    
    application = ApplicationBuilder().token("5479638961:AAGHwR_QcXmiEEZQWwDXmljPfRP_sqvkb5I").build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.add_handler(CommandHandler('mychar', mychar))
    
    application.add_handler(CommandHandler('shifr', shifr))
    
    application.add_handler(CommandHandler('deshifr', deshifr))
    
    application.add_handler(CommandHandler('setpass', setpass))
    
    application.add_handler(CommandHandler('hentai', hentai))
    
    application.add_handler(CommandHandler('calc', calc))
    
    application.add_handler(CommandHandler('maze', maze))
    
    application.add_handler(CommandHandler('ranword', random_command))
    
    application.add_handler(CommandHandler('ranum', random_num))
    
    application.add_handler(CommandHandler('ruletka', ruletka))
    
    application.add_handler(CommandHandler('hesoyam', hesoyam))
    
    application.add_handler(CommandHandler('help', help_1))
    
    application.add_handler(CommandHandler('news', news))
    
    application.add_handler(CommandHandler('badapple', badapple))
    
    application.add_handler(CommandHandler('clean', clean))
    
    application.add_handler(CommandHandler('rumors', rumors))
    
    application.add_handler(CommandHandler('capital', capital))
    
    application.add_handler(CommandHandler('bible', bible))
    
    application.add_handler(CommandHandler('rumors_all', rumors_all))
   
    application.run_polling()