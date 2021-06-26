import config
import telebot
import requests
from openpyxl import Workbook
from openpyxl import load_workbook
from bs4 import BeautifulSoup as BS
from telebot import types
from PIL import Image

class Category:
    subCategories = []
    def __init__(self, name): 
        self.name = "%s" % name

class SubCategory:
    def __init__(self, name): 
        self.name = "%s" % name
        self.products = []

class Products:
    def __init__(self, name, description, price, img): 
        self.name = "%s" % name
        self.description = description
        self.price = price
        self.img = img

wb = load_workbook('file.xlsx')
ws = wb.active


category = []

for i, row in enumerate(ws.values):
    if i == 0:
        continue
    c = row[0]
    if i >= 141 or c == "" or c == '' or c == 'None' or c == "None":
        break
    index = 0
    z = True
    for k, j in enumerate(category):
        if j.name == c:
            index = k
            z = False
            break
    if z:
        index = len(category)
        category.append(Category(c))
        category[index].subCategories = []
    have = False
    subCategoryIndex = 0
    subCategoryName = row[1]
    for k, j in enumerate(category[index].subCategories):
        if j.name == "%s" % subCategoryName:
            have = True
            
            subCategoryIndex = k
            break
    if not have:
        subCategoryIndex = len(category[index].subCategories)
        category[index].subCategories.append(SubCategory(subCategoryName))
        category[index].subCategories[subCategoryIndex].products = []
    name = row[2]
    description = row[3]
    price = row[4]
    image = row[5]
    category[index].subCategories[subCategoryIndex].products.append(Products(name, description, price, image))



bot  = telebot.TeleBot(config.token)


def removeProbel(message) -> str:
    strs = message.split()
    a = ''
    for i in strs:
        a = a+i+' '
    return a

@bot.message_handler(commands=['start'])
def main(message):
  
    markup = types.ReplyKeyboardMarkup()

    categoryButtons = []
    for i in category:
        categoryButtons.append(types.KeyboardButton("%s" % i.name))
    i=0
    while i < len(categoryButtons):
        if i+1 == len(categoryButtons):
            markup.row(categoryButtons[i])
        elif i+2 == len(categoryButtons):
            markup.row(categoryButtons[i], categoryButtons[i+1])
        else:
            markup.row(categoryButtons[i], categoryButtons[i+1], categoryButtons[i+2])
        i += 3

    bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
 ,reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    markup = types.ReplyKeyboardMarkup()

    categoryButtons = []
    for i in category:
        categoryButtons.append(types.KeyboardButton(i.name))

    j=0
    while j < len(category):
        if message.text == "%s" % category[j].name :
            buttons = []
            for s in category[j].subCategories:
                buttons.append(types.KeyboardButton("%s" % s.name))
            index=0
            while index < len(buttons):
                if index+1 == len(buttons):
                    markup.row(buttons[index])
                elif index+2 == len(buttons):
                    markup.row(buttons[index], buttons[index+1])
                else:
                    markup.row(buttons[index], buttons[index+1], buttons[index+2])
                index += 3
            markup.row(types.KeyboardButton('🏠 Главное меню'))
            bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
            ,reply_markup=markup)
            return
        j+=1
    
    j=0
    while j < len(category):
        for s in category[j].subCategories:
            # print(f'text {message.text} and {s.name}   {"%s" % s.name == message.text}')
            if message.text == "%s" % s.name:
                buttons = []
                for m in s.products:
                    buttons.append(types.KeyboardButton(m.name))
                index=0
                while index < len(buttons):
                    if index+1 == len(buttons):
                        markup.row(buttons[index])
                    elif index+2 == len(buttons):
                        markup.row(buttons[index], buttons[index+1])
                    else:
                        markup.row(buttons[index], buttons[index+1], buttons[index+2])
                    index += 3
                markup.row(types.KeyboardButton("🏠 Главное меню"))
                bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
                ,reply_markup=markup)
                return
        j+=1

    buttons = []
    j=0
    while j < len(category):
        for s in category[j].subCategories:
            for m in s.products:
                if message.text == "%s" % m.name:
                    try:
                        bot.send_photo( message.chat.id, open("%s" % m.img , "rb"), removeProbel(m.description))
                    except:
                        print(f'no such file {m.img}')
                        bot.send_message(message.chat.id, removeProbel(m.description))
                    return
        j+=1


    if message.text == "🏠 Главное меню":
        i=0
        while i < len(categoryButtons):
            if i+1 == len(categoryButtons):
                markup.row(categoryButtons[i])
            elif i+2 == len(categoryButtons):
                markup.row(categoryButtons[i], categoryButtons[i+1])
            else:
                markup.row(categoryButtons[i], categoryButtons[i+1], categoryButtons[i+2])
            i += 3

        bot.send_message(message.chat.id, "Выбрать категории",reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)
