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
                        bot.send_photo( message.chat.id, open("%s" % m.img , "rb"), m.description)
                    except:
                        print(f'no such file {m.img}')
                        bot.send_message(message.chat.id, m.description)
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
    # if message.text == "СТИРАЛЬНЫЕ МАШИНЫ" : 
    #     markup.row(itembtn10, itembtn11, itembtn12)  
    #     markup.row(itembtn13)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)
    
    # if message.text == "МИКРОВОЛНОВАЯ ПЕЧЬ" : 
    #     markup.row(itembtn14, itembtn15)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)
    
    # if message.text == "ДУХОВАЯ ПЕЧЬ" : 
    #     markup.row(itembtn16, itembtn17 )
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "КОНДИЦИОНЕРЫ" : 
    #     markup.row(itembtn18, itembtn19, itembtn20)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "ВЫТЯЖКА" : 
    #     markup.row( itembtn21, itembtn22)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "МОНИТОР" : 
    #     markup.row( itembtn23, itembtn24)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "ВАРОЧНЫЕ ПАНЕЛИ" : 
    #     markup.row( itembtn25, itembtn26)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "Телевизор" : 
    #     markup.row( itembtn27, itembtn28, itembtn29)
    #     markup.row( itembtn30, itembtn31)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "Газовая плита" : 
    #     markup.row( itembtn32, itembtn33, itembtn34)
    #     markup.row( itembtn35, itembtn36)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "10kg" :
    #     markup.row(itembtn37, itembtn38, itembtn39)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "8kg" :
    #     markup.row(itembtn40, itembtn41, itembtn42)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "7kg" :
    #     markup.row(itembtn43)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "6kg" :
    #     markup.row(itembtn44, itembtn45)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "25l" :
    #     markup.row (itembtn46)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "26l" :
    #     markup.row (itembtn47)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "75l" :
    #     markup.row (itembtn48)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "70l" :
    #     markup.row (itembtn49 , itembtn50, itembtn51)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "12" :
    #     markup.row (itembtn52, itembtn53, itembtn54)  
    #     markup.row(itembtn55, itembtn56,itembtn57)  
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "18" :
    #     markup.row (itembtn58, itembtn59, itembtn60)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "24" :
    #     markup.row(itembtn61, itembtn62, itembtn63)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "Peramida" :
    #     markup.row(itembtn64, itembtn65, itembtn66)  
    #     markup.row(itembtn67)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "Glass" :
    #     markup.row (itembtn68)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "22" :
    #     markup.row (itembtn69)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "27" :
    #     markup.row(itembtn70, itembtn71)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "4" :
    #     markup.row(itembtn72, itembtn73, itembtn74)  
    #     markup.row(itembtn75, itembtn76)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "5" :
    #     markup.row(itembtn77, itembtn78, itembtn79)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "43" :
    #     markup.row(itembtn80)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "50" :
    #     markup.row(itembtn81, itembtn82)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "55" :
    #     markup.row(itembtn83)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "65" :
    #     markup.row(itembtn84, itembtn85)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "75" :
    #     markup.row(itembtn97)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "A" :
    #     markup.row(itembtn86, itembtn87, itembtn88)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "B" :
    #     markup.row(itembtn89, itembtn90, itembtn91)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "C" :
    #     markup.row(itembtn92, itembtn93)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "E" :
    #     markup.row(itembtn94)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)

    # if message.text == "F" :
    #     markup.row(itembtn95)
    #     markup.row(itembtn96)
    #     bot.send_message(message.chat.id, "Salom "+message.from_user.first_name +" bu bot orqali siz IMMER mahsulotlari haqida malumotga ega bo'lasiz kerakli mahsulot turini tanlang"
    #     ,reply_markup=markup)
        
    # if message.text == "IW100-14686BLS" : 
    #     bot.send_photo( message.chat.id, open("file/IW100-14686BLS1.jpg" , "rb"), "Максимальная загрузка 10 кг \nКласс энергосбережения A \nУровень шума при стирке 58 dB \nРазмеры продукта 600 × 565 × 850 мм \nКоличество программ 16 \nУровень шума при отжиме 15 минут \nБлокировка от детей Есть \nРасход воды (при полной загрузке) Есть \nРасход воды (при частичной загрузке) Есть \nВес Есть \nКласс стирки Ozone technology \nТип мотора Инвертор \nDisplay type Сенсор")

    # if message.text == "IW100-14596BLX" : 
    #     bot.send_photo(  message.chat.id , open("file/IW100-14596BLX1.jpg" ,  "rb" ) , "Максимальная загрузка 10 кг  \nМакс скорость отжима 1400rpm \nКласс энергосбережения A \nУровень шума при стирке 58 dB \nРазмеры продукта 600 × 565 × 850 мм \nКоличество программ 16 \nУровень шума при отжиме 15 минут \nБлокировка от детей Есть \nРасход воды (при полной загрузке) Есть \nРасход воды (при частичной загрузке) Есть \nВес Есть \nКласс стирки Ozone technology \nТип мотора Инвертор \nDisplay type Сенсор" )
    
    # if message.text == "IW80- 14586BX" : 
    #     bot.send_photo( message.chat.id, open("file/586 dark grey.jpg" , "rb") , "Максимальная загрузка 8 кг \nМакс скорость отжима 1400rpm \nКласс энергосбережения A \nУровень шума при стирке 58 dB \nРазмеры продукта 600 ×450 × 850 mm \nКоличество программ 16 \nУровень шума при отжиме 15 минут \nБлокировка от детей Есть \nРасход воды (при полной загрузке) Есть \nРасход воды (при частичной загрузке) Есть \nВес Есть \nКласс стирки - Тип мотора Инвертор \n Display type LED" )
   
    # if message.text ==  "IFK80-S1400W" : 
    #    bot.send_photo( message.chat.id, open("file/IFK80-S1400W.jpg" , "rb"), "Максимальная загрузка 8 kg \nМакс скорость отжима 1400rpm \nКласс энергосбережения A+++ \nУровень шума при стирке 59 dB \nРазмеры продукта 595 × 470 × 850 \nКоличество программ 16 \nУровень шума при отжиме 78 dB \nБлокировка от детей Есть \nРасход воды (при полной загрузке) 54 л \nРасход воды (при частичной загрузке) 45 л \nВес 63 кг \nКласс стирки A \nТип мотора Универсал \nDisplay type LED")

    # if message.text == "IFC80-S1401SDSS" : 
    #     bot.send_photo( message.chat.id, open("file/IFC80-S1401SDSS.jpg" , "rb"), "Максимальная загрузка  8 kg \nМакс скорость отжима  1400rpm \nКласс энергосбережения  A+++ \nУровень шума при стирке  59 dB \nРазмеры продукта  595 × 470 × 850 \nКоличество программ  16 \nУровень шума при отжиме  78 dB \nБлокировка от детей  Есть \nРасход воды (при полной загрузке)  54 л \nРасход воды (при частичной загрузке)  45 л \nВес  63 кг \nКласс стирки  A \nТип мотора  Универсал \nDisplay type  LED")

    # if message.text == "IFG70-S1412S" : 
    #     bot.send_photo( message.chat.id, open("file/IFG70-S1412S.jpg" , "rb"), "Максимальная загрузка  7 кг \nМакс скорость отжима  1400rpm \nКласс энергосбережения  A+++ \nУровень шума при стирке  59 dB \nРазмеры продукта  595 × 495 × 850 \nКоличество программ  15 \nУровень шума при отжиме  78 dB \nБлокировка от детей  Есть \nРасход воды (при полной загрузке)  50 л \nРасход воды (при частичной загрузке)  42 л \nВес  61 кг \nКласс стирки  A \nТип мотора  Универсал \nDisplay type  LED")
    
    # if message.text == "IFG60-S1003S" : 
    #     bot.send_photo( message.chat.id, open("file/IFG60-S1003S.jpg" , "rb"), "Максимальная загрузка  6 кг \nМакс скорость отжима  1000rpm \nКласс энергосбережения  A++ \nУровень шума при стирке  58 dB \nРазмеры продукта  595 × 470 × 850 \nКоличество программ  16 \nУровень шума при отжиме  74 dB \nБлокировка от детей  Есть \nРасход воды (при полной загрузке)  48 л \nРасход воды (при частичной загрузке)  37 л \nВес  54 кг \nКласс стирки  A \nТип мотора  Универсал \nDisplay type  LED")

    # if message.text == "IFE60-S1006S" : 
    #     bot.send_photo( message.chat.id, open("file/IFE60-S1006S.jpg" , "rb"), "Максимальная загрузка  6 кг \nМакс скорость отжима  1000rpm \nКласс энергосбережения  A++ \nУровень шума при стирке  59 dB \nРазмеры продукта  595 × 470 × 850 \nКоличество программ  23 \nУровень шума при отжиме  74 dB \nБлокировка от детей  Есть \nРасход воды (при полной загрузке)  47 л \nРасход воды (при частичной загрузке)  38 л \nВес  54 кг \nКласс стирки  A \nТип мотора  Универсал \nDisplay type  Нет")
        
    # if message.text == "IFG80-S1412S" : 
    #     bot.send_photo( message.chat.id, open("file/IFG80-S1412S.jpg" , "rb"), "Максимальная загрузка	8 кг \nМакс скорость отжима	1400rpm \nКласс энергосбережения	A+++-20% \nУровень шума при стирке	59 dB \nРазмеры продукта	595 × 475 × 850 \nКоличество программ	15 \nУровень шума при отжиме	76 dB \nБлокировка от детей	Есть \nРасход воды (при полной загрузке)	54 л \nРасход воды (при частичной загрузке)	47 л \nВес	63кг \nКласс стирки	A \nТип мотора	Инвертер \nDisplay type	LED")
        
    # if message.text == "IFG80-S1412S" : 
    #     bot.send_photo( message.chat.id, open("file/IFG80-S1412S.jpg" , "rb"), "Максимальная загрузка	8 кг \nМакс скорость отжима	1400rpm \nКласс энергосбережения	A+++-20% \nУровень шума при стирке	59 dB \nРазмеры продукта	595 × 475 × 850 \nКоличество программ	15 \nУровень шума при отжиме	76 dB \nБлокировка от детей	Есть \nРасход воды (при полной загрузке)	54 л \nРасход воды (при частичной загрузке)	47 л \nВес	63кг \nКласс стирки	A \nТип мотора	Инвертер \nDisplay type	LED")

    # if message.text == "IFG70-S1412S" : 
    #     bot.send_photo( message.chat.id, open("file/IFG70-S1412S.jpg" , "rb"), "Максимальная загрузка	7 кг \nМакс скорость отжима	1400rpm \nКласс энергосбережения	A+++ \nУровень шума при стирке	59 dB \nРазмеры продукта	595 × 495 × 850 \nКоличество программ	15 \nУровень шума при отжиме	78 dB \nБлокировка от детей	Есть \nРасход воды (при полной загрузке)	50 л \nРасход воды (при частичной загрузке)	42 л \nВес	61 кг \nКласс стирки	A \nТип мотора	Универсал \nDisplay type	LED")
        
    # if message.text == "AG925B2V" : 
    #     bot.send_photo( message.chat.id, open("file/AG925B2V.jpg" , "rb"), "Объём	25 Л \nМощность	900 Вт \nТип установки	Встраиваемая \nВнутреннее покрытие камеры	Из нержавеющей стали \nТип управления	Электронное управление \nБлокировка от детей	Есть \nДисплей	Есть \nТаймер	Есть \nРежим разморозки	Есть \nВес	17,6 кг \nРазмеры продукта	594×403×382")
        
    # if message.text == "TG925HN6" : 
    #     bot.send_photo( message.chat.id, open("file/TG925HN6.jpg" , "rb"), "Объём	25 Л \nМощность	900 Вт \nТип установки	Встраиваемая \nВнутреннее покрытие камеры	Из нержавеющей стали \nТип управления	Сенсорное /nБлокировка от детей	Есть /nДисплей	Есть /nТаймер	Есть /nРежим разморозки	Есть /nВес	18,5 кг /nРазмеры продукта	595×400×388")
        
    # if message.text == "I65M40M1-45" : 
    #     bot.send_photo( message.chat.id, open("file/FS-AB-05.jpg" , "rb"), "Тип духовки	Электрическая независимая \nОбъём	75 Л \nКласс энергосбережения	A \nТип управления	механическое управление \nПереключатели	Поворотные \nТаймер	Есть \nДисплей	Нет \nГриль	Есть \nЦвет корпуса	Чёрный \nКоличество функций	4 \nРазмеры продукта	595 x 575 x 595")
        
    # if message.text == "I65M80M1-B2" : 
    #     bot.send_photo( message.chat.id, open("file/FS-AB-06.jpg" , "rb"), "Тип духовки	Электрическая независимая \nОбъём	70 Л /nКласс энергосбережения	A /nТип управления	механическое управление /nПереключатели	Поворотные /nТаймер	Есть /nДисплей	Нет /nГриль	Есть /nЦвет корпуса	Чёрный /nКоличество функций	8 /nРазмеры продукта	595 x 575 x 595")
        
    # if message.text == "I65M90E3-18" : 
    #     bot.send_photo( message.chat.id, open("file/FS-AB-07.jpg" , "rb"), "Тип духовки	Электрическая независимая \nОбъём	70 Л \nКласс энергосбережения	A \nТип управления	Механическое и сенсорное управление \nПереключатели	Поворотные \nТаймер	Есть \nДисплей	Есть \nГриль	Есть \nЦвет корпуса	Чёрный \nКоличество функций	9 \nРазмеры продукта	595 x 575 x 595")
        
    # if message.text == "I65M90T0-11" : 
    #     bot.send_photo( message.chat.id, open("file/FS-AB-08.jpg" , "rb"), "Тип духовки	Электрическая независимая \nОбъём	70 Л \nКласс энергосбережения	A \nТип управления	Сенсорное управление \nПереключатели	Сенсорное \nТаймер	Есть \nДисплей	Есть \nГриль	Есть \nЦвет корпуса	Чёрный \nКоличество функций	9 \nРазмеры продукта	595 x 575 x 595")
        
    # if message.text == "Trendi 12" : 
    #     bot.send_photo( message.chat.id, open("file/trendi-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система \nОбслуживаемая площадь	36 кв.м \nИнвертор	Нет \nОсновные режимы	охлаждение / обогрев \nКласс энергопотребления	A \nМощность в режиме охлаждения	3590 Вт \nМощность в режиме обогрева	3690 Вт \nУровень шума внутреннего блока	43 дБ \nУровень шума внешнего блока	53 дБ \nТип хладагента	R410A \nОбъем воздушного потока	590 м3/ч \nВес внутреннего блока	9 кг \nВес внешнего блока	28 кг")
        
    # if message.text == "Desert 12" : 
    #     bot.send_photo( message.chat.id, open("file/desert-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система \nОбслуживаемая площадь	36 кв.м \nИнвертор	Нет \nОсновные режимы	охлаждение / обогрев \nКласс энергопотребления	A \nМощность в режиме охлаждения	3590 Вт \nМощность в режиме обогрева	3690 Вт \nУровень шума внутреннего блока	43 дБ \n Уровень шума внешнего блока	53 дБ \nТип хладагента	R410A \nОбъем воздушного потока	590 м3/ч \nВес внутреннего блока	9 кг \nВес внешнего блока	28 кг")
        
    # if message.text == "FRENZI 12" : 
    #     bot.send_photo( message.chat.id, open("file/frenzi-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система \nОбслуживаемая площадь	36 кв.м \nИнвертор	Нет \nОсновные режимы	охлаждение / обогрев \nКласс энергопотребления	A \nМощность в режиме охлаждения	3590 Вт \nМощность в режиме обогрева	3690 Вт \nУровень шума внутреннего блока	43 дБ \nУровень шума внешнего блока	53 дБ \nТип хладагента	R410A \nОбъем воздушного потока	590 м3/ч \nВес внутреннего блока	9 кг \nВес внешнего блока	28 кг")
        
    # if message.text == "Brase 12" : 
    #     bot.send_photo( message.chat.id, open("file/brase-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система \nОбслуживаемая площадь	36 кв.м \nИнвертор	Нет \nОсновные режимы	охлаждение / обогрев \nКласс энергопотребления	A \nМощность в режиме охлаждения	3400 Вт \nМощность в режиме обогрева	3400 Вт \nУровень шума внутреннего блока	43 дБ \nУровень шума внешнего блока	54 дБ \nТип хладагента	R410A \nОбъем воздушного потока	630 м3/ч \nВес внутреннего блока	11 кг \nВес внешнего блока	29 кг")
        
    # if message.text == "DarkMoon 12" : 
    #     bot.send_photo( message.chat.id, open("file/darkmoon-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система \nОбслуживаемая площадь	36 кв.м\nИнвертор	Есть\nОсновные режимы	охлаждение / обогрев\nКласс энергопотреблеaния	A\nМощность в режиме охлаждения	3050 Вт\nМощность в режиме обогрева	3250 Вт\nУровень шума внутреннего блока	42 дБ\nУровень шума внешнего блока	53 дБ\nТип хладагента	R410A\nОбъем воздушного потока	600 м3/ч\nВес внутреннего блока	8,50 кг\nВес внешнего блока	25 кг")
        
    # if message.text == "TurboChili 12" : 
    #     bot.send_photo( message.chat.id, open("file/turbochill-12.jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	36 кв.м\nИнвертор	Есть\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	3050 Вт\nМощность в режиме обогрева	3250 Вт\nУровень шума внутреннего блока	42 дБ\nУровень шума внешнего блока	53 дБ\nТип хладагента	R410A\nОбъем воздушного потока	600 м3/ч\nВес внутреннего блока	8,50 кг\nВес внешнего блока	25 кг")
         
    # if message.text == "Trendi 18" : 
    #     bot.send_photo( message.chat.id, open("file/trendi-12 (1).jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	54 кв.м\nИнвертор	Нет\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	5350 Вт\nМощность в режиме обогрева	5650 Вт\nУровень шума внутреннего блока	46 дБ\nУровень шума внешнего блока	55 дБ\nТип хладагента	R410A\nОбъем воздушного потока	970 м3/ч\nВес внутреннего блока	12 кг\nВес внешнего блока	36 кг")
        
    # if message.text == "Frenzi 18" : 
    #     bot.send_photo( message.chat.id, open("file/frenzi-12 (1).jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	54 кв.м\nИнвертор	Нет\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	5350 Вт\nМощность в режиме обогрева	5650 Вт\nУровень шума внутреннего блока	46 дБ\nУровень шума внешнего блока	55 дБ\nТип хладагента	R410A\nОбъем воздушного потока	970 м3/ч\nВес внутреннего блока	12 кг\nВес внешнего блока	36 кг")
        
    # if message.text == "DarkMoon18" : 
    #     bot.send_photo( message.chat.id, open("file/darkmoon-12 (1).jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	54 кв.м\nИнвертор	Есть\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	5200 Вт\nМощность в режиме обогрева	5400 Вт\nУровень шума внутреннего блока	46 дБ\nУровень шума внешнего блока	54 дБ\nТип хладагента	R410A\nОбъем воздушного потока	900 м3/ч\nВес внутреннего блока	12 кг\nВес внешнего блока	35 кг")
        
    # if message.text == "Desert24" : 
    #     bot.send_photo( message.chat.id, open("file/desert-12 (1).jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	72 кв.м\nИнвертор	Нет\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	7000 Вт\nМощность в режиме обогрева	7300 Вт\nУровень шума внутреннего блока	48 дБ\nУровень шума внешнего блока	58 дБ\nТип хладагента	R410A\nОбъем воздушного потока	1200 м3/ч\nВес внутреннего блока	16 кг\nВес внешнего блока	49,5 кг")
        
    # if message.text == "DarkMoon24" : 
    #     bot.send_photo( message.chat.id, open("file/darkmoon-12 (2).jpg" , "rb"), "Тип кондиционера	Настенная сплит-система\nОбслуживаемая площадь	72 кв.м\nИнвертор	Есть\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	7100 Вт\nМощность в режиме обогрева	7300 Вт\nУровень шума внутреннего блока	62 дБ\nУровень шума внешнего блока	66 дБ\nТип хладагента	R410A\nОбъем воздушного потока	1250 м3/ч\nВес внутреннего блока	14 кг\nВес внешнего блока	46 кг")
        
    # if message.text == "Pillar24" : 
    #     bot.send_photo( message.chat.id, open("file/pillar-24.jpg" , "rb"), "Тип кондиционера	Колонная сплит-система\nОбслуживаемая площадь	72 кв.м\nИнвертор	Нет\nОсновные режимы	охлаждение / обогрев\nКласс энергопотребления	A\nМощность в режиме охлаждения	7150 Вт\nМощность в режиме обогрева	7600 Вт\nУровень шума внутреннего блока	54 дБ\nУровень шума внешнего блока	58 дБ\nТип хладагента	R410A\nОбъем воздушного потока	1120 м3/ч\nВес внутреннего блока	38 кг\nВес внешнего блока	51 кг")
    
    # if message.text == "M201" : 
    #     bot.send_photo( message.chat.id, open("file/M201.png" , "rb"), "Material	Нержавеющая сталь\nMotor power	65 Вт\nMaximum air flow	300 м3/ч\nLighting	LED лампа\nCharcoal filter	Есть\nProduct dimensions	598 x 452 x 180\nControl type	Кнопочное\nAir outlet	150 mm\nNoise level	65 dB\nNumber of speeds	3")
                        
    # if message.text == "M202" : 
    #     bot.send_photo( message.chat.id, open("file/M202.png" , "rb"), "Material	Нержавеющая сталь\nMotor power	330 Вт\nMaximum air flow	1150 м3/ч\nLighting	LED лампа\nCharcoal filter	Есть\nProduct dimensions	600 x 500 x 700\nControl type	Кнопочное\nAir outlet	150 mm\nNoise level	66 dB\nNumber of speeds	3")
        
    # if message.text == "M203" : 
    #     bot.send_photo( message.chat.id, open("file/M203.jpg" , "rb"), "Material	Нержавеющая сталь\nMotor power	330 Вт\nMaximum air flow	1150 м3/ч\nLighting	LED лампа\nCharcoal filter	Есть\nProduct dimensions	602 x 500 x 700\nControl type	Кнопочное\nAir outlet	150 mm\nNoise level	66 dB\nNumber of speeds	3")
        
    # if message.text == "M204" : 
    #     bot.send_photo( message.chat.id, open("file/M204.png" , "rb"), "Material	Нержавеющая сталь\nMotor power	330 Вт\nMaximum air flow	1150 м3/ч\nLighting	LED лампа\nCharcoal filter	Есть\nProduct dimensions	600 x 500 x 700\nControl type	Серсорное\nAir outlet	150 mm\nNoise level	65 dB\nNumber of speeds	3")
                    
    # if message.text == "M205" : 
    #     bot.send_photo( message.chat.id, open("file/M205.png" , "rb"), "Material	Нержавеющая сталь и закаленное стекло\nMotor power	330 Вт\nMaximum air flow	1150 м3/ч\nLighting	LED лампа\nCharcoal filter	Есть\nProduct dimensions	660 x 500 x 460\nControl type	Серсорное\nAir outlet	150 mm\nNoise level	65 dB\nNumber of speeds	3")
            
    # if message.text == "22D8000 21.5" : 
    #     bot.send_photo( message.chat.id, open("file/22D8000-4.jpg" , "rb"), "Тип	ЖК-монитор, широкоформатный\nДиагональ	21.5\nРазрешение	1920 x 1080 (16:9)\nТип матрицы экрана	IPS\nЯркость	220 кд/м2\nКонтрастность	5000000: 1\nВремя отклика	5 мс\nУгол обзора	178°(В) x 178°(Г)\nКоличество цветов	16.7 млн.\nПорты	VGA + HDMI\nДинамик	Нет\nПотребляемая мощность	21 Вт\nОсобенности	-\nЧастота обновления кадров	60 Гц")
            
    # if message.text == "27F9000 27" : 
    #     bot.send_photo( message.chat.id, open("file/27F9000-4.jpg" , "rb"), "Тип	ЖК-монитор, широкоформатный\nДиагональ	27\nРазрешение	1920 x 1080 (16:9)\nТип матрицы экрана	IPS\nЯркость	220 кд/м2\nКонтрастность	5000000: 1\nВремя отклика	5 мс\nУгол обзора	178°(В) x 178°(Г)\nКоличество цветов	16.7 млн.\nПорты	VGA + HDMI\nДинамик	Нет\nПотребляемая мощность	30 Вт\nОсобенности	Подсветка без мерцания, FreeSync\nЧастота обновления кадров	60 Гц")
            
    # if message.text == "Curved 27G9000 27" : 
    #     bot.send_photo( message.chat.id, open("file/27G9000-4.jpg" , "rb"), "Тип	Игровой, широкоформатный, Изогнутый\nДиагональ	27 FULL HD\nРазрешение	1920 x 1080 (16:9)\nТип матрицы экрана	IPS\nЯркость	250 кд/м2\nКонтрастность	5000000: 1\nВремя отклика	1 мс\nУгол обзора	178°(В) x 178°(Г)\nКоличество цветов	16.7 млн.\nПорты	VGA+HDMI+DP+AUDIO\nДинамик	2\nПотребляемая мощность	35 Вт\nОсобенности	Подсветка без мерцания, FreeSync\nЧастота обновления кадров	144 Гц")
            
    # if message.text == "S100" : 
    #     bot.send_photo( message.chat.id, open("file/S100.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	нержавеющая сталь\nРазмеры продукта	590 x 510 x 90\nЦвет корпуса	Металлическое, Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G101" : 
    #     bot.send_photo( message.chat.id, open("file/G101.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 110\nЦвет корпуса	Серый\nЭлектроподжиг	Имеется")
            
    # if message.text == "G102" : 
    #     bot.send_photo( message.chat.id, open("file/G102.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 97\nЦвет корпуса	Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G103" : 
    #     bot.send_photo( message.chat.id, open("file/G103.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 101\nЦвет корпуса	Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G104" : 
    #     bot.send_photo( message.chat.id, open("file/G104.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 90\nЦвет корпуса	Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G105" : 
    #     bot.send_photo( message.chat.id, open("file/G105 (1).jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 90\nЦвет корпуса	Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G106" : 
    #     bot.send_photo( message.chat.id, open("file/G106.jpg" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	Закаленное стекло\nРазмеры продукта	600 x 510 x 90\nЦвет корпуса	Чёрный\nЭлектроподжиг	Имеется")
            
    # if message.text == "G107" : 
    #     bot.send_photo( message.chat.id, open("file/G107.png" , "rb"), "Тип панели	Газовая\nКоличество конфорок	4\nТип управления	Механическое\nТип установки	Встраиваемая\nМатериал рабочей поверхности	нержавеющая сталь\nРазмеры продукта	600 x 510 x 89\nЦвет корпуса	Металлическое\nЭлектроподжиг	Имеется")
            
    # if message.text == "43ME750S" : 
    #     bot.send_photo( message.chat.id, open("file/43ME750S.jpg" , "rb"), "Диагональ	43'(108CM)\nРазрешение	1920*1080 full hd\nФормат экрана	16:9\nАкустическая система	2 Колонок\nМощность звука	Без Рамки\nТип ТВ	Full HD Smart\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	\nВес с подставкой	")
            
    # if message.text == "50ME650U" : 
    #     bot.send_photo( message.chat.id, open("file/50ME650U.jpg" , "rb"), "Диагональ	50'(126SM)\nРазрешение	1920*1080 full hd\nФормат экрана	16:9\nАкустическая система	2 Колонок\nМощность звука	-\nТип ТВ	ULTRA HD 4K Smart\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	\nВес с подставкой	")

    # if message.text == "50ME8500 4K UHD" : 
    #     bot.send_photo( message.chat.id, open("file/50ME8500.jpg" , "rb"), "Диагональ	50' (127 см)\nРазрешение	3840x2160 4K UHD\nФормат экрана	16:9\nАкустическая система	Два динамика\nМощность звука	16 Вт (2х8 Вт)\nТип ТВ	UHD Smart TV\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	MPG,MPEG,MPEG2-PS,MP4,MKV,AVI,ASF,FLV,MP3,JPEG,PNG,BMP\nВес с подставкой	13.8 кг")

    # if message.text == "55ME650U" : 
    #     bot.send_photo( message.chat.id, open("file/50ME650U (1).jpg" , "rb"), "Диагональ	50'(139СМ)\nРазрешение	1920*1080 full hd\nФормат экрана	16:9\nАкустическая система	2 Колонок\nМощность звука	-\nТип ТВ	ULTRA HD 4K Smart\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	\nВес с подставкой")

    # if message.text == "65ME650U" : 
    #     bot.send_photo( message.chat.id, open("file/50ME650U (2).jpg" , "rb"), "Диагональ	65'(164SM)\nРазрешение	1920*1080 full hd\nФормат экрана	16:9\nАкустическая система	2 Колонок\nМощность звука	-\nТип ТВ	ULTRA HD 4K Smart\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	\nВес с подставкой	")

    # if message.text == "65ME8500 4K UHD" : 
    #     bot.send_photo( message.chat.id, open("file/65ME8500.jpg" , "rb"), "Диагональ	65' (164 см)\nРазрешение	3840x2160 4K UHD\nФормат экрана	16:9\nАкустическая система	Два динамика\nМощность звука	16 Вт (2х8 Вт)\nТип ТВ	UHD Smart TV\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x3, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	MPG,MPEG,MPEG2-PS,MP4,MKV,AVI,ASF,FLV,MP3,JPEG,PNG,BMP\nВес с подставкой	22 кг")

    # if message.text == "75ME6500 4K UHD" : 
    #     bot.send_photo( message.chat.id, open("file/75ME6500.jpg" , "rb"), "Диагональ	75' (189 см)\nРазрешение	3840x2160 4K UHD\nФормат экрана	16:9\nАкустическая система	Два динамика\nМощность звука	2х15 Вт\nТип ТВ	UHD Smart TV\nПоддержка DVB-T2	Есть\nПоддержка DVB-C	Есть\nПоддержка DVB-S	Есть\nПоддержка DVB-S2	Есть\nПоддержка DVB-T	Есть\nВходы	AV, HDMI x4, USB x2, Ethernet (RJ-45), Wi-Fi 802.11ac, CI\nПоддерживаемые форматы	MPG,MPEG,MPEG2-PS,MP4,MKV,AVI,ASF,FLV,MP3,JPEG,PNG,BMP\nВес с подставкой	26 кг")

    # if message.text == "A01" : 
    #     bot.send_photo( message.chat.id, open("file/a01.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электриктирческая\nАвто огнетушитель	Есть\nСистема управления газом духовки	Есть\nКоличество конфорок	4\nТип управления	Механический\nРазмер Духовки	64 литр\nТип решетки	Стальной\nТип крышки	Стекло\nЛампа накаливания духовки	Есть\nСъемное внутреннее стекло духовки	Есть\nЦвет	Металлик\nМеханический таймер	Есть\nИзоляция духовки canuf	Есть")

    # if message.text == "A02" : 
    #     bot.send_photo( message.chat.id, open("file/a02.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	4\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Инокс\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")

    # if message.text == "A02E" : 
    #     bot.send_photo( message.chat.id, open("file/a02e.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	3\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Инокс\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")

    # if message.text == "B01" : 
    #     bot.send_photo( message.chat.id, open("file/b01.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и Электрический\nАвто огнетушитель	Есть\nСистема управления газом духовки	Есть\nКоличество конфорок	4\nТип управления	Механический\nРазмер Духовки	64 литр\nТип решетки	Стальной\nТип крышки	Стекло\nЛампа накаливания духовки	Есть\nСъемное внутреннее стекло духовки	Есть\nЦвет	Черный\nМеханический таймер	Есть\nИзоляция духовки canuf	Есть")

    # if message.text == "B01E" : 
    #     bot.send_photo( message.chat.id, open("file/b01e.png" , "rb"), "Варочная поверхность	\nДуховка	\nАвто огнетушитель	\nСистема управления газом духовки	\nКоличество конфорок	\nТип управления	\nРазмер Духовки	\nТип решетки	\nТип крышки	\nЛампа накаливания духовки	\nСъемное внутреннее стекло духовки	\nЦвет	\nМеханический таймер	\nИзоляция духовки canuf")

    # if message.text == "B02" : 
    #     bot.send_photo( message.chat.id, open("file/b02.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	4\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Черный\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")

    # if message.text == "C01" : 
    #     bot.send_photo( message.chat.id, open("file/c01.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электрический\nАвто огнетушитель	Есть\nСистема управления газом духовки	Есть\nКоличество конфорок	4\nТип управления	Механический\nРазмер Духовки	64 литр\nТип решетки	Стальной\nТип крышки	Стекло\nЛампа накаливания духовки	Есть\nСъемное внутреннее стекло духовки	Есть\nЦвет	Темно серый\nМеханический таймер	Есть\nИзоляция духовки canuf	Есть")

    # if message.text == "C02" : 
    #     bot.send_photo( message.chat.id, open("file/c02.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	4\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Антрацид\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")

    # if message.text == "E01" : 
    #     bot.send_photo( message.chat.id, open("file/e01.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	4\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Белый\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")

    # if message.text == "F01" : 
    #     bot.send_photo( message.chat.id, open("file/f01.png" , "rb"), "Варочная поверхность	Газ\nДуховка	Газ и электричество\nАвто огнетушитель	Имеется\nСистема управления газом духовки	Имеется\nКоличество конфорок	4\nТип управления	Механическая\nРазмер Духовки	64 литр\nТип решетки	Чугун\nТип крышки	Стекло\nЛампа накаливания духовки	Имеется\nСъемное внутреннее стекло духовки	Имеется\nЦвет	Черный\nМеханический таймер	Имеется\nИзоляция духовки canuf	Имеется")


if __name__ == '__main__':
    bot.polling(none_stop=True)