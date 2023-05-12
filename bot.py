import json, time
import telebot
from threading import Thread
from telebot import types
from main import check

config_data = json.loads(open("./config.json", "r").read())
bot = telebot.TeleBot(
    token=config_data["telegram_bot_token"], parse_mode="html")

def checker():
    while True:
        data = json.loads(open("./config.json", "r").read())
        for word in data['words']:
            sites = check(word, data['white_list'])
            msg = f'{word} -> \n'
            for s in sites:
                msg = msg + s + "\n"
            bot.send_message(data["admin_chat_id"], msg)
        time.sleep(config_data['check_time'])
starter = Thread(target=checker)



def add_white(url):
    old = json.loads(open("./config.json", "r").read())
    old['white_list'].append(url.text)
    newf = open("./config.json", "w")
    newf.write(json.dumps(old))
    newf.close()
    bot.reply_to(url, "added.")


def del_white(url):
    old = json.loads(open("./config.json", "r").read())
    if url.text in old['white_list']:
        old['white_list'].remove(url.text)
        newf = open("./config.json", "w")
        newf.write(json.dumps(old))
        newf.close()
        bot.reply_to(url, "removed.")
    else:
        bot.reply_to(url, "this url not fund.")


def add_word(word):
    old = json.loads(open("./config.json", "r").read())
    old['words'].append(word.text)
    newf = open("./config.json", "w")
    newf.write(json.dumps(old))
    newf.close()
    bot.reply_to(word, "added.")


def del_word(word):
    old = json.loads(open("./config.json", "r").read())
    if word.text in old['words']:
        old['words'].remove(word.text)
        newf = open("./config.json", "w")
        newf.write(json.dumps(old))
        newf.close()
        bot.reply_to(word, "removed.")
    else:
        bot.reply_to(word, "this word not fund.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('white sites')
    itembtn2 = types.KeyboardButton('word list')
    itembtn3 = types.KeyboardButton('add white site')
    itembtn3_5 = types.KeyboardButton('add word')
    itembtn4 = types.KeyboardButton('delete white site')
    itembtn4_5 = types.KeyboardButton('delete word')
    s1 = types.KeyboardButton('start')
    s2 = types.KeyboardButton('stop')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn3_5, itembtn4, itembtn4_5, s1, s2)
    bot.reply_to(message, "Howdy, how are you doing?", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):

    if message.text == "white sites":
        data = json.loads(open("./config.json", "r").read())
        msg = "->\n"
        for site in data['white_list']:
            msg = msg + site + "\n"
        bot.send_message(message.chat.id, msg)

    elif message.text == "word list":
        data = json.loads(open("./config.json", "r").read())
        msg = "->\n"
        for site in data['words']:
            msg = msg + site + "\n"
        bot.send_message(message.chat.id, msg)

    elif message.text == "add white site":
        sent = bot.reply_to(message, "sent site url:")
        bot.register_next_step_handler(sent, add_white)

    elif message.text == "add word":
        sent = bot.reply_to(message, "sent word:")
        bot.register_next_step_handler(sent, add_word)

    elif message.text == "delete white site":
        sent = bot.reply_to(message, "sent url:")
        bot.register_next_step_handler(sent, del_white)
    
    elif message.text == "delete word":
        sent = bot.reply_to(message, "sent word:")
        bot.register_next_step_handler(sent, del_word)
    
    elif message.text == "start":
        starter.start()
        bot.reply_to(message, "started")
    
    elif message.text == "stop":
        starter.terminate()
        bot.reply_to(message, "stoped")


bot.infinity_polling()
