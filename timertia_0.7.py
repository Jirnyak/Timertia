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
import math
import pandas as pd
import matplotlib.pyplot as plt

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

def market_mult(fond):
    return 1000000000/(float(fond)+1)
   
def prix(good):   
    return 1000/math.sqrt(int(good)+1)
   
def maintain(army1, army2, army3):
    return 1 + (int(army1)+int(army2)+int(army3)+1)/10000
   
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
 
'''
 
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
                players_list1[j+1] = str(stats[0])
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
   
'''
   
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
            #time.sleep(1)
            money = float(players_list[k+1])
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
        players.write(str(update.effective_user.id) + "\n" + str(10000) + "\n" + "1000\n" + "1000\n" + "1000\n")
        players.close()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + str(1000) + "$ R: 0"  + " G: 0"  + " B: 0" ))
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
            y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\gold.png', 'rb'), caption="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + money + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
            messages.append(y.message_id) 
            break
    if found == 0:
        players = open('players.txt', 'a', encoding="utf-8")
        players.write(str(update.effective_user.id) + "\n" + str(10000) + "\n" + "1000\n" + "1000\n" + "1000\n")
        players.close()
        moneys = open('money_buffer.txt', 'w', encoding="utf-8")
        moneys.write("1000")
        moneys.close()
        os.system("capital.py 1")
        y = await context.bot.send_photo(update.effective_chat.id, photo=open('G:\Timertia_bot\gold.png', 'rb'), caption="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + "1000" +  "$s R: 0"  + " G: 0"  + " B: 0")
        messages.append(y.message_id)
 
async def market(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /market " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    #date = datetime.datetime.utcnow().timestamp()
    market = open('market.txt', 'r', encoding="utf-8")
    market_list = market.read().splitlines()
    market.close()
    FOND = market_mult(market_list[3])
    prix_R = prix(market_list[0])*FOND
    prix_G = prix(market_list[1])*FOND
    prix_B = prix(market_list[2])*FOND
    pd.read_table('market_log.txt', parse_dates = False, index_col = 0, sep = ',').plot()
    plt.savefig(fname='stonk.png')
    plt.close()
    y = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('G:\Timertia_bot\stonk.png', 'rb'), caption=("Господин, " + str(update.effective_user.first_name) + ", состояние рынка:\n" + "R: "  + str(prix_R) + "\nG: " + str(prix_G) + "\nB: " + str(prix_B) + "\nМировой Фонд: " + str(market_list[3])))
    messages.append(y.message_id)
    
async def buy(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /buy " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    message = str(update.effective_message.text)
    message = message.replace("/buy@timertia_bot ","")
    message = message.replace("/buy ","")
    message = message.replace("/buy@timertia_bot","")
    message = message.replace("/buy","")
    players = open('players.txt', 'r', encoding="utf-8")
    players_list = players.read().splitlines()
    players.close()
    market = open('market.txt', 'r', encoding="utf-8")
    market_list = market.read().splitlines()
    market.close()
    FOND = market_mult(market_list[3])
    prix_R = prix(market_list[0])*FOND
    prix_G = prix(market_list[1])*FOND
    prix_B = prix(market_list[2])*FOND
    amount = [int(s) for s in message.split() if s.isdigit()]
    amount = amount[0]
    found = 0
    for k in range(len(players_list)):
        if str(update.effective_user.id) == players_list[k]:
            found = 1
            if ("r" in message or "R" in message) and int(market_list[0])-amount >= 0 and float(players_list[k+1]) - amount*prix_R > 0:
                players_list[k+1] = str(float(players_list[k+1]) - amount*prix_R)
                players_list[k+2] = str(int(players_list[k+2]) + amount)
                market_list[0] = str(int(market_list[0])-amount)
                market_list[3] = str(float(market_list[3]) + amount*prix_R)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id) 
            elif ("g" in message or "R" in message) and int(market_list[1])-amount >= 0 and float(players_list[k+1]) - amount*prix_G > 0:
                players_list[k+1] = str(float(players_list[k+1]) - amount*prix_G)
                players_list[k+3] = str(int(players_list[k+3]) + amount)
                market_list[1] = str(int(market_list[1]) - amount)
                market_list[3] = str(float(market_list[3]) + amount*prix_G)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id) 
            elif ("b" in message or "B" in message) and int(market_list[2])-amount >= 0 and float(players_list[k+1]) - amount*prix_B > 0:
                players_list[k+1] = str(float(players_list[k+1]) - amount*prix_B)
                players_list[k+4] = str(int(players_list[k+4]) + amount)
                market_list[2] = str(int(market_list[2]) - amount)
                market_list[3] = str(float(market_list[3]) + amount*prix_B)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id) 
            else:
                y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", транзакция неудачна!"))
                messages.append(y.message_id)
            players = open('players.txt', 'r', encoding="utf-8")
            players_list1 = players.read().splitlines()
            players.close()
            for j in range(len(players_list1)):
                if str(update.effective_user.id) == players_list1[j]:
                    players_list1[j+1] = players_list[k+1]
                    players_list1[j+2] = players_list[k+2]
                    players_list1[j+3] = players_list[k+3]
                    players_list1[j+4] = players_list[k+4]
                    players = open('players.txt', 'w', encoding="utf-8")
                    longlist = ""
                    for l in range(len(players_list1)):
                        longlist += (players_list1[l]+"\n")
                    players.write(longlist)
                    players.close()  
                    break
                else:
                    None
            market = open('market.txt', 'r', encoding="utf-8")
            market_list1 = market.read().splitlines()
            market.close()
            market_list1[0] = market_list[0]
            market_list1[1] = market_list[1]
            market_list1[2] = market_list[2]
            market_list1[3] = market_list[3]
            market = open('market.txt', 'w', encoding="utf-8")
            longlist = ""
            for l in range(len(market_list1)):
                longlist += (market_list1[l]+"\n")
            market.write(longlist)
            market.close()  
            break
    if found == 0:
        players = open('players.txt', 'a', encoding="utf-8")
        players.write(str(update.effective_user.id) + "\n" + str(1000) + "\n" + "0\n" + "0\n" + "0\n")
        players.close()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + str(1000) + "$ R: 0"  + " G: 0"  + " B: 0" ))
        messages.append(y.message_id)
    market_count = open('market_count.txt', 'r', encoding="utf-8")
    market_count_list = market_count.read().splitlines()
    market_count.close()
    market_count_list[0] = str(int(market_count_list[0])+1)
    market_count = open('market_count.txt', 'w', encoding="utf-8")
    market_count.write(market_count_list[0])
    market_count.close()
    market_log = open("market_log.txt", 'a', encoding="utf-8")
    market_log.write("\n" + market_count_list[0] + "," + str(prix_R) + "," +str(prix_G) + "," + str(prix_B))
    market_log.close()
 
async def sell(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /sell " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    message = str(update.effective_message.text)
    message = message.replace("/sell@timertia_bot ","")
    message = message.replace("/sell ","")
    message = message.replace("/sell@timertia_bot","")
    message = message.replace("/sell","")
    players = open('players.txt', 'r', encoding="utf-8")
    players_list = players.read().splitlines()
    players.close()
    market = open('market.txt', 'r', encoding="utf-8")
    market_list = market.read().splitlines()
    market.close()
    FOND = market_mult(market_list[3])
    prix_R = prix(market_list[0])*FOND
    prix_G = prix(market_list[1])*FOND
    prix_B = prix(market_list[2])*FOND
    amount = [int(s) for s in message.split() if s.isdigit()]
    amount = amount[0]
    found = 0
    for k in range(len(players_list)):
        if str(update.effective_user.id) == players_list[k]:
            found = 1
            if ("r" in message or "R" in message) and int(players_list[k+2])-amount >= 0 and float(market_list[3])-0.9*amount*prix_R > 0:
                players_list[k+1] = str(float(players_list[k+1]) + 0.9*amount*prix_R)
                players_list[k+2] = str(int(players_list[k+2]) - amount)
                market_list[0] = str(int(market_list[0]) + amount)
                market_list[3] = str(float(market_list[3]) - 0.9*amount*prix_R)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id) 
            elif ("g" in message or "G" in message) and int(players_list[k+3])-amount >= 0 and float(market_list[3]) - 0.9*amount*prix_G > 0:
                players_list[k+1] = str(float(players_list[k+1]) + 0.9*amount*prix_G)
                players_list[k+3] = str(int(players_list[k+3]) - amount)
                market_list[1] = str(int(market_list[1]) + amount)
                market_list[3] = str(float(market_list[3]) - 0.9*amount*prix_G)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id) 
            elif ("b" in message or "B" in message) and int(players_list[k+4])-amount >= 0 and float(market_list[3]) - 0.9*amount*prix_B > 0:
                players_list[k+1] = str(float(players_list[k+1]) + 0.9*amount*prix_B)
                players_list[k+4] = str(int(players_list[k+4]) - amount)
                market_list[2] = str(int(market_list[2])+amount)
                market_list[3] = str(float(market_list[3]) - 0.9*amount*prix_B)
                y = await context.bot.send_message(update.effective_chat.id, text="Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[k+1] + "$ R: " + players_list[k+2] + " G: " + players_list[k+3] + " B: " + players_list[k+4])
                messages.append(y.message_id)
            else:
                y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", транзакция неудачна!"))
                messages.append(y.message_id)
            players = open('players.txt', 'r', encoding="utf-8")
            players_list1 = players.read().splitlines()
            players.close()
            for j in range(len(players_list1)):
                if str(update.effective_user.id) == players_list1[j]:
                    players_list1[j+1] = players_list[k+1]
                    players_list1[j+2] = players_list[k+2]
                    players_list1[j+3] = players_list[k+3]
                    players_list1[j+4] = players_list[k+4]
                    players = open('players.txt', 'w', encoding="utf-8")
                    longlist = ""
                    for l in range(len(players_list1)):
                        longlist += (players_list1[l]+"\n")
                    players.write(longlist)
                    players.close()  
                    break
                else:
                    None
            market = open('market.txt', 'r', encoding="utf-8")
            market_list1 = market.read().splitlines()
            market.close()
            market_list1[0] = market_list[0]
            market_list1[1] = market_list[1]
            market_list1[2] = market_list[2]
            market_list1[3] = market_list[3]
            market = open('market.txt', 'w', encoding="utf-8")
            longlist = ""
            for l in range(len(market_list1)):
                longlist += (market_list1[l]+"\n")
            market.write(longlist)
            market.close()  
            break
    if found == 0:
        players = open('players.txt', 'a', encoding="utf-8")
        players.write(str(update.effective_user.id) + "\n" + str(1000) + "\n" + "0\n" + "0\n" + "0\n")
        players.close()
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Господин, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + str(1000) + "$ R: 0"  + " G: 0"  + " B: 0" ))
        messages.append(y.message_id)
    market_count = open('market_count.txt', 'r', encoding="utf-8")
    market_count_list = market_count.read().splitlines()
    market_count.close()
    market_count_list[0] = str(int(market_count_list[0])+1)
    market_count = open('market_count.txt', 'w', encoding="utf-8")
    market_count.write(market_count_list[0])
    market_count.close()
    market_log = open("market_log.txt", 'a', encoding="utf-8")
    market_log.write("\n" + market_count_list[0] + "," + str(prix_R) + "," +str(prix_G) + "," + str(prix_B))
    market_log.close()
    
async def build(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /build " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    message = str(update.effective_message.text)
    message = message.replace("/build@timertia_bot ","")
    message = message.replace("/build ","")
    message = message.replace("/build@timertia_bot","")
    message = message.replace("/build","")
    generals = open('generals.txt', 'r', encoding="utf-8")
    generals_list = generals.read().splitlines()
    generals.close()
    players = open('players.txt', 'r', encoding="utf-8")
    players_list = players.read().splitlines()
    players.close()
    market = open('market.txt', 'r', encoding="utf-8")
    market_list = market.read().splitlines()
    market.close()
    FOND = market_mult(market_list[3])
    prix_R = prix(market_list[0])*FOND
    prix_G = prix(market_list[1])*FOND
    prix_B = prix(market_list[2])*FOND
    amount = [int(s) for s in message.split() if s.isdigit()]
    amount = amount[0]
    found1 = 0
    found2 = 0
    for a in range(len(players_list)):
        if str(update.effective_user.id) == players_list[a]:
            found1 = 1
            break
        else:
            None
    for b in range(len(generals_list)):
        if str(update.effective_user.id) == generals_list[b]:
            found2 = 1
            break
        else:
            None
    if found1 == 1 and found2 == 1:
        if ("r" in message or "R" in message) and int(players_list[a+2])-amount >= 0 and float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]) > 0:
                players_list[a+1] = str(float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                players_list[a+2] = str(int(players_list[a+2]) - amount)
                market_list[3] = str(float(market_list[3]) + amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                generals_list[b+2] = str(int(generals_list[b+2]) + amount)
                y = await context.bot.send_message(update.effective_chat.id, text="Генерал, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[a+1] + "$ R: " + players_list[a+2] + " G: " + players_list[a+3] + " B: " + players_list[a+4])
                messages.append(y.message_id) 
        elif ("g" in message or "G" in message) and int(players_list[a+3])-amount >= 0 and float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4])  > 0:
                players_list[a+1] = str(float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                players_list[a+3] = str(int(players_list[a+3]) - amount)
                market_list[3] = str(float(market_list[3]) + amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                generals_list[b+3] = str(int(generals_list[b+3]) + amount)
                y = await context.bot.send_message(update.effective_chat.id, text="Генерал, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[a+1] + "$ R: " + players_list[a+2] + " G: " + players_list[a+3] + " B: " + players_list[a+4])
                messages.append(y.message_id) 
        elif ("b" in message or "B" in message) and int(players_list[a+4])-amount >= 0 and float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4])  > 0:
                players_list[a+1] = str(float(players_list[a+1]) - amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                players_list[a+4] = str(int(players_list[a+4]) - amount)
                market_list[3] = str(float(market_list[3]) + amount*maintain(generals_list[b+2],generals_list[b+3],generals_list[b+4]))
                generals_list[b+4] = str(int(generals_list[b+4]) + amount)
                y = await context.bot.send_message(update.effective_chat.id, text="Генерал, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[a+1] + "$ R: " + players_list[a+2] + " G: " + players_list[a+3] + " B: " + players_list[a+4])
                messages.append(y.message_id)
        elif ("exp" in message or "EXP" in message) and float(players_list[b+5]) - amount > 0 and float(market_list[3]) - float(players_list[b+5]) > 0:
                players_list[a+1] = str(float(players_list[a+1]) + float(players_list[b+5]))
                market_list[3] = str(float(market_list[3]) - float(players_list[b+5]))
                generals_list[b+5] = str(int(generals_list[b+5]) - amount)
                y = await context.bot.send_message(update.effective_chat.id, text="Генерал, " + str(update.effective_user.first_name) + ", ваш капитал:\n" + players_list[a+1] + "$ R: " + players_list[a+2] + " G: " + players_list[a+3] + " B: " + players_list[a+4])
                messages.append(y.message_id) 
        else:
                y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Генерал, " + str(update.effective_user.first_name) + ", строительство невозможно!"))
                messages.append(y.message_id)
        players = open('players.txt', 'r', encoding="utf-8")
        players_list1 = players.read().splitlines()
        players.close()
        for j in range(len(players_list1)):
            if str(update.effective_user.id) == players_list1[j]:
                players_list1[j+1] = players_list[a+1]
                players_list1[j+2] = players_list[a+2]
                players_list1[j+3] = players_list[a+3]
                players_list1[j+4] = players_list[a+4]
                players = open('players.txt', 'w', encoding="utf-8")
                longlist = ""
                for l in range(len(players_list1)):
                    longlist += (players_list1[l]+"\n")
                players.write(longlist)
                players.close()  
                break
            else:
                None
        generals = open('generals.txt', 'r', encoding="utf-8")
        generals_list1 = generals.read().splitlines()
        generals.close()
        longlist = ""
        for d in range(len(generals_list1)):
            if str(update.effective_user.id) == generals_list1[d]:
                generals_list1[d+2] = generals_list[b+2]
                generals_list1[d+3] = generals_list[b+3]
                generals_list1[d+4] = generals_list[b+4]
                generals_list1[d+5] = generals_list[b+5]
                generals = open('generals.txt', 'w', encoding="utf-8")
                longlist = ""
                for p in range(len(generals_list1)):
                    longlist += (generals_list1[p]+"\n")
                generals.write(longlist)
                generals.close()  
                break
            else:
                None
        market = open('market.txt', 'r', encoding="utf-8")
        market_list1 = market.read().splitlines()
        market.close()
        market_list1[0] = market_list[0]
        market_list1[1] = market_list[1]
        market_list1[2] = market_list[2]
        market_list1[3] = market_list[3]
        market = open('market.txt', 'w', encoding="utf-8")
        longlist = ""
        for l in range(len(market_list1)):
            longlist += (market_list1[l]+"\n")
        market.write(longlist)
        market.close()  
        market_count = open('market_count.txt', 'r', encoding="utf-8")
        market_count_list = market_count.read().splitlines()
        market_count.close()
        market_count_list[0] = str(int(market_count_list[0])+1)
        market_count = open('market_count.txt', 'w', encoding="utf-8")
        market_count.write(market_count_list[0])
        market_count.close()
        market_log = open("market_log.txt", 'a', encoding="utf-8")
        market_log.write("\n" + market_count_list[0] + "," + str(prix_R) + "," +str(prix_G) + "," + str(prix_B))
        market_log.close()
        war_count = open('war_count.txt', 'r', encoding="utf-8")
        war_count_list = war_count.read().splitlines()
        war_count.close()
        war_count = open('war_count.txt', 'w', encoding="utf-8")
        war_count.write(str(int(war_count_list[0])+1))
        war_count.close()      
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=(str(update.effective_user.first_name) + ", вы не выбрали сторону (/side) или не зарегистрировались на бирже (/capital)!"))
        messages.append(y.message_id)
 
async def war(update, context):
    global admin
    admin_id = admin[0]
    log.write("\n" + str(datetime.datetime.now()) +" /war " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    war_count = open('war_count.txt', 'r', encoding="utf-8")
    war_count_list = war_count.read().splitlines()
    war_count.close()
    counter = 0
    generals = open('generals.txt', 'r', encoding="utf-8")
    generals_list = generals.read().splitlines()
    generals.close()
    market = open('market.txt', 'r', encoding="utf-8")
    market_list = market.read().splitlines()
    market.close()
    if int(war_count_list[0]) > 10:
        war_count = open('war_count.txt', 'w', encoding="utf-8")
        war_count.write("0")
        war_count.close()
        RU_R = 0
        RU_G = 0 
        RU_B = 0
        NA_R = 0
        NA_G = 0
        NA_B = 0 
        for i in range(len(generals_list)):
            if generals_list[i] == "РФ":
                RU_R += int(generals_list[i+1])
                RU_G += int(generals_list[i+2])
                RU_B += int(generals_list[i+3])
            elif generals_list[i] == "NATO":
                NA_R += int(generals_list[i+1])
                NA_G += int(generals_list[i+2])
                NA_B += int(generals_list[i+3])
            else: 
                None
        RU_R_b = RU_R - 10*NA_B
        if RU_R_b < 0:
            RU_R_b = 0
        RU_G_b = RU_G - 10*NA_R
        if RU_G_b < 0:
            RU_G_b = 0
        RU_B_b = RU_B - 10*NA_G
        if RU_B_b < 0:
            RU_B_b = 0
        NA_R_b = NA_R - 10*RU_B
        if NA_R_b < 0:
            NA_R_b = 0
        NA_G_b = NA_G - 10*RU_R
        if NA_G_b < 0:
            NA_G_b = 0
        NA_B_b = NA_B - 10*RU_G
        if NA_B_b < 0:
            NA_B_b = 0
        RU_total_b = RU_R_b + RU_G_b + RU_B_b
        NA_total_b = NA_R_b + NA_G_b + NA_B_b
        FINAL = RU_total_b - NA_total_b
        TOTAL = RU_R + RU_G + RU_B + NA_R + NA_G + NA_B
        if FINAL > 0 or (RU_R > NA_R and RU_G > NA_G and RU_B > NA_B):
            for i in range(len(generals_list)):
                if generals_list[i] == "РФ":
                    counter += 1
                    generals_list[i+1] = "0"
                    generals_list[i+2] = "0"
                    generals_list[i+3] = "0"
                elif generals_list[i] == "NATO":
                    generals_list[i+1] = "0"
                    generals_list[i+2] = "0"
                    generals_list[i+3] = "0"
            for i in range(len(generals_list)):
                if generals_list[i] == "РФ":
                    generals_list[i+4] = str(float(generals_list[i+4]) + TOTAL/counter)
            y = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('G:\Timertia_bot\rf_flag.jpg', 'rb'),  caption =("РФ ОДЕРЖАЛА ПОБЕДУ!" + "\nСилы РФ: " + str(RU_G*100) +  " пехоты " + str(RU_B*10) +  " бронетехники " + str(RU_R) +  " артиллерии " + "\nСилы NATO: " + str(NA_G*100) +  " пехоты " + str(NA_B*10) +  " бронетехники " + str(NA_R) +  " артиллерии "))
            messages.append(y.message_id)
        elif FINAL < 0 or (RU_R < NA_R and RU_G < NA_G and RU_B < NA_B):
            for i in range(len(generals_list)):
                if generals_list[i] == "NATO":
                    counter += 1
                    generals_list[i+1] = "0"
                    generals_list[i+2] = "0"
                    generals_list[i+3] = "0"
                elif generals_list[i] == "РФ":
                    generals_list[i+1] = "0"
                    generals_list[i+2] = "0"
                    generals_list[i+3] = "0"
            for i in range(len(generals_list)):
                if generals_list[i] == "NATO":
                    generals_list[i+4] = str(float(generals_list[i+4]) + TOTAL/counter)
            y = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('G:\Timertia_bot\nato_flag.jpg', 'rb'),  caption = ("НАТО ОДЕРЖАЛО ПОБЕДУ!" + "\nСилы РФ: " + str(RU_G*100) +  " пехоты " + str(RU_B*10) +  " бронетехники " + str(RU_R) +  " артиллерии " + "\nСилы NATO: " + str(NA_G*100) +  " пехоты " + str(NA_B*10) +  " бронетехники " + str(NA_R) +  " артиллерии "))
            messages.append(y.message_id)
        else:
            y = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('G:\Timertia_bot\white_flag.png', 'rb'),  caption = ("НИЧЬЯ!" + "\nСилы РФ: " + str(RU_G*100) +  " пехоты " + str(RU_B*10) +  " бронетехники " + str(RU_R) +  " артиллерии " + "\nСилы NATO: " + str(NA_G*100) +  " пехоты " + str(NA_B*10) +  " бронетехники " + str(NA_R) +  " артиллерии "))
            messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text=("Война начнётся через " + str(10 - int(war_count_list[0])) + " строительств юнитов."))
        messages.append(y.message_id)
    longlist = ""
    for i in range(len(generals_list)):
        longlist += (generals_list[i]+"\n")
    generals = open('generals.txt', 'w', encoding="utf-8")
    generals.write(longlist)
    generals.close()
        
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
    
async def ask(update, context):
    message = str(update.effective_message.text)
    message = message.replace("/ask@timertia_bot ","")
    message = message.replace("/ask ","")
    message = message.replace("/ask@timertia_bot","")
    message = message.replace("/ask","")
    message = message.replace("?","")
    message_list = message.split(" ")
    answer = random.randint(0,1)
    if answer == 1:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text= "Да, потому что " + random.choice(message_list) + ".")
        messages.append(y.message_id)
    else:
        y = await context.bot.send_message(chat_id=update.effective_chat.id, text= "Нет, потому что " + random.choice(message_list) + ".")
        messages.append(y.message_id)      
    log.write("\n" + str(datetime.datetime.now()) + " /ask " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
 
async def anon(update, context):
    message = str(update.effective_message.text)
    message = message.replace("/anon ","")
    message = message.replace("/anon ","")
    message = message.replace("/anon@timertia_bot","")
    message = message.replace("/anon","")
    y = await context.bot.send_message(chat_id=-1001696329294, text=message)
    messages.append(y.message_id)
 
async def rumors_all(update, context):
    y = await context.bot.send_document(chat_id=update.effective_chat.id, document=open('G:\Timertia_bot\mrumors.txt', 'rb'), filename="rumors.txt")
    messages.append(y.message_id)
    
async def side(update, context):
    log.write("\n" + str(datetime.datetime.now()) +" /side " + str(update.effective_user.first_name) + " " + str(update.effective_user.last_name) + " " + str(update.effective_user.id))
    message = str(update.effective_message.text)
    generals = open('generals.txt', 'r', encoding="utf-8")
    generals_list = generals.read().splitlines()
    generals.close()
    found = 0
    for k in range(len(generals_list)):
        if str(update.effective_user.id) == generals_list[k]:
            found = 1
            army = generals_list[k+1]
            R = str((generals_list[k+2]))
            G = str(int(generals_list[k+3])*100)
            B = str(int(generals_list[k+4])*10)
            EXP = str((generals_list[k+5]))
            y = await context.bot.send_message(update.effective_chat.id, text="Генерал " + army + " " + str(update.effective_user.first_name) + ", у вас:\n" + R + " артиллерии\n" + G + " пехоты\n" + B + " бронетехники\n" + EXP + " опыта\n")
            messages.append(y.message_id) 
            break
    if found == 0:
        if "ru" in message:
            generals = open('generals.txt', 'a', encoding="utf-8")
            generals.write(str(update.effective_user.id) + "\n" + "РФ" + "\n" + "10" +  "\n"  + "10" +  "\n"  + "10" +  "\n" + "0" +  "\n")
            generals.close()
            y = await context.bot.send_message(update.effective_chat.id, text="Генерал " + "РФ" + " " + str(update.effective_user.first_name) + ", у вас:\n" + "0" + " артиллерии\n" + "0" + " пехоты\n" + "0" + " бронетехники\n")
            messages.append(y.message_id) 
        elif "na" in message:
            generals = open('generals.txt', 'a', encoding="utf-8")
            generals.write(str(update.effective_user.id) + "\n" + "NATO" + "\n" + "10" +  "\n"  + "10" +  "\n"  + "10" +  "\n" + "0" +  "\n")
            generals.close()
            y = await context.bot.send_message(update.effective_chat.id, text="Генерал " + "NATO" + " " + str(update.effective_user.first_name) + ", у вас:\n" + "0" + " артиллерии\n" + "0" + " пехоты\n" + "0" + " бронетехники\n")
            messages.append(y.message_id)
        else:
            y = await context.bot.send_message(update.effective_chat.id, text="Введите <b>ru</b> или <b>nato</b> для выбора стороны!" , parse_mode="HTML")
            messages.append(y.message_id)
    else:
        None
                         
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
    + ".\n/hesoyam <b>пароль число</b> - даю денег <s>ОТКЛЮЧЕНО</s>" 
    + ".\n/capital - показываю ваш капитал"
    + ".\n/market - показываю рыночные цены на rgb"
    + ".\n/buy <b>r g b</b> <b>количество</b> - покупаю rgb на рынке" 
    + ".\n/sell <b>r g b</b> <b>количество</b> - продаю rgb на рынке" 
    + ".\n/build <b>r g b</b> <b>количество</b> - произвожу юниты" 
    + ".\n/side <b>ru</b> или <b>nato</b> - назначаю вас генералом соотвествующей стороны" 
    + ".\n/war - симулирую войну РФ с НАТО" 
    + ".\n/news - сообщаю свежие новости" 
    + ".\n/badapple <b>пароль</b> - дудошу чат аниме <s>ОТКЛЮЧЕНО</s>" 
    + ".\n<tg-spoiler>/hentai  <b>пароль</b> - показываю кое-что</tg-spoiler>" 
    + ".\n/rumors - рассказываю анонимные слухи (если ввести сообщение, то добавлю его к слухам)" 
    + ".\n/rumors_all - высылаю txt со всеми слухами"
    + ".\n/bible - цитирую Библию" 
    + ".\n/ask <b>вопрос</b> - отвечаю на вопрос"
    + ".\n/anon <b>текст</b> - отправляю анонимное сообщение в конфу (эффективно со страницы бота)"     
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
    
    application = ApplicationBuilder().token("TOKEN").build()
    
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
    
    #application.add_handler(CommandHandler('hesoyam', hesoyam))
    
    application.add_handler(CommandHandler('help', help_1))
    
    application.add_handler(CommandHandler('news', news))
    
    application.add_handler(CommandHandler('badapple', badapple))
    
    application.add_handler(CommandHandler('clean', clean))
    
    application.add_handler(CommandHandler('rumors', rumors))
    
    application.add_handler(CommandHandler('capital', capital))
    
    application.add_handler(CommandHandler('bible', bible))
    
    application.add_handler(CommandHandler('rumors_all', rumors_all))
    
    application.add_handler(CommandHandler('ask', ask))
    
    application.add_handler(CommandHandler('anon', anon))
    
    application.add_handler(CommandHandler('side', side))
    
    application.add_handler(CommandHandler('market', market))
    
    application.add_handler(CommandHandler('buy', buy))
    
    application.add_handler(CommandHandler('sell', sell))
    
    application.add_handler(CommandHandler('build', build))
    
    application.add_handler(CommandHandler('war', war))
   
    application.run_polling()