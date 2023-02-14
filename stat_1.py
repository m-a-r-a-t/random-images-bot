import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('STAT_BOT_TOKEN')


def get_count_users():
    all_users_records = []
    with open("users.txt", "r") as fin:
        for line in fin:
            match = re.findall(r'Жду свою валентинку', line)[0]
            if len(match) > 0:
                line = line.split(' ')[0]
                all_users_records.append(line)

    uniq_users = {}
    for record in all_users_records:
        if record not in uniq_users:
            uniq_users[record] = 1

    return len(uniq_users)


bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'count'])
def send_welcome(message):
    try:
        count = get_count_users()
        bot.send_message(message.chat.id,  f"Пользователей: {count}")
    except:
        bot.send_message(message.chat.id,  f"Что-то пошло не так...")


bot.infinity_polling()
