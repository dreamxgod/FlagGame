from curses import KEY_A1
from tkinter import RIGHT
from aiogram import Bot, Dispatcher, executor,types
import random
import time
from PIL import Image
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
global answer
global false_number
global false_answer
def global_modify():
    global button_inline1
    global button_inline2
    global keyboard_inline
    global num

def right_answer(num):
    if num == 1:
        answer = "Canada"
    elif num == 2:
        answer = "Ukraine" 
    elif num ==3:
        answer = "Andorra"
    elif num == 4:
        answer = "Angola" 
    elif num == 5:
        answer = "Argentina"
    return  answer 

def false_number_function(num):
    number = 1
    while number == num:
        number = random.randrange(1,5)
    return number    

def false_answer_function(false_number):
    if false_number == 1:
        false_answer = "Canada"
    elif false_number == 2:
        false_answer = "Ukraine" 
     


    return false_answer


def num_func():
    num  = random.randrange(1,5)
    answer = right_answer(num)
    false_number = false_number_function(num)
    false_answer = false_answer_function(false_number)
    button_inline1 = InlineKeyboardButton(text = answer, callback_data=answer)
    button_inline2 = InlineKeyboardButton( text = false_answer, callback_data=false_answer) 
    keyboard_inline = InlineKeyboardMarkup().add(button_inline1, button_inline2)





bot = Bot(token='5536823787:AAGYsFBVz1WVS_3kBPZQ9MKCAOSTBUw-1zY')
dp = Dispatcher(bot)



button1 = KeyboardButton('/continue')
button2 = KeyboardButton('end')
button5 = KeyboardButton('/know')
button6 = KeyboardButton('/dontknow')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2).add(button5).add(button6)

global_modify()
num_func()
  
        

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hello! Im FlagGame Bot. Yyou can play with me" )

@dp.message_handler(commands=['go'])
async def flag_function(message: types.Message):
    num1 = 2
    if num1 == 1:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/canada.png', 'rb'))
        await message.reply("rrfrf", reply_markup=keyboard1)
    elif num1 ==2:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/ukraine.png', 'rb'))
        await message.reply("Lets start! ", reply_markup=keyboard1)

@dp.message_handler(commands=['continue'])
async def flag_answer(message: types.Message ):
    num_func()
    if num == 1:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/canada.png', 'rb'))
        await message.reply("Here is a new  country for you", reply_markup=keyboard1)
    elif num ==2:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/ukraine.png', 'rb'))  
        await message.reply("Here is a new  country for you", reply_markup=keyboard1)
    if num == 3:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/andorra.png', 'rb'))
        await message.reply("Here is a new  country for you", reply_markup=keyboard1)
    elif num ==4:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/angola.png', 'rb'))  
        await message.reply("Here is a new  country for you", reply_markup=keyboard1)    
    elif num == 5:
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Users/ivankalinets/Documents/KPI/programming /FlagGame/pictures/argentina.png', 'rb'))  
        await message.reply("Here is a new  country for you", reply_markup=keyboard1) 
        
     
@dp.message_handler(commands=['know'])
async def know_function(message: types.Message):
    await message.reply("Select a flag:", reply_markup=keyboard_inline)
    

@dp.callback_query_handler(text=[answer, false_answer])
async def random_value(call: types.CallbackQuery):
    if call.data == answer:
        await call.message.answer('You are right')
        await call.message.reply("Lets continue", reply_markup=keyboard1)
    if call.data == false_answer:
        await call.message.answer('You are wrong')
        await call.message.reply("Lets continue", reply_markup=keyboard1)
    await call.answer()

executor.start_polling(dp)


 