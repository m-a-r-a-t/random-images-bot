import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import os
import random
from dotenv import load_dotenv
from text import Txt

txt = Txt()
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = AsyncTeleBot(BOT_TOKEN, parse_mode=None)
now_users = {}

markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn = types.KeyboardButton(txt.wait_btn)
markup.add(btn)


def throttling(chat_id, typee=0):

    if typee == 0:
        if chat_id in now_users:
            if now_users[chat_id] >= 1:
                return False
            now_users[chat_id] += 1
        else:
            now_users[chat_id] = 1

        return True
    else:
        now_users[chat_id] = -1


def get_random_video():
    name = random.choice(os.listdir('./videos'))
    video = open('./videos/'+name, 'rb')
    return video


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    with open("users.txt", "a") as myfile:
        myfile.write(f"{message.chat.id} {message.text}\n")
    await bot.send_message(message.chat.id, txt.start_msg, reply_markup=markup)


@bot.message_handler(regexp=txt.main_handler_regx)
async def send_random_video(message):
    try:
        ok = throttling(message.chat.id)
        with open("users.txt", "a") as myfile:
            myfile.write(f"{message.chat.id} {message.text}\n")
        if not ok:
            return

        video = get_random_video()
        preview = await bot.send_message(message.chat.id, txt.preview_msg, reply_markup=markup)
        await bot.send_video(message.chat.id, video, reply_markup=markup)
        video.close()

        throttling(message.chat.id, 1)

    except Exception as e:
        print("Ошибка", e)
        await bot.send_message(message.chat.id, "Что-то пошло не так...", reply_markup=markup)


asyncio.run(bot.infinity_polling())
