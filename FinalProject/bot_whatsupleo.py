# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
import markovify
import json
import flask
import os

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url="https://whatsupleo.herokuapp.com/bot")

app = flask.Flask(__name__)

#генерируем сообщение из предложений, созданных с помощью Марковской цепи
def markov_mess():
    with open('text_all.txt', encoding='utf-8') as f:
        text = f.read()
    text_model = markovify.Text(text, state_size=3)
    message = ' '
    for i in range(random.randint(2, 5)):
        message = message + text_model.make_short_sentence(140, tries=100) + ' '
    return message

#отвечаем на сообщения \help и \start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Лев Толстой. Секрет успеха", url="https://vk.com/public98293549")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Лев Николаевич Толстой пишет вам письма: рассказывает, о чём думал на досуге и как живёт. Не философствованием единым! Он стремится быть с корреспондентами на одной волне, поэтому готов и новости из «Коммерсанта» обсудить, и процитировать что-нибудь из омского панка.\n\r\n\rБот поможет получать столько писем, сколько пожелаете. Просто начните общение! Помните, что письма не пишутся в одно мгновение, и будьте терпеливы.\n\r\n\r_«Я около месяца болею и теперь очень слаб, и потому письмо мое так бессвязно и бестолково».\n\rПисьмо к Е. В. Арцимович, 2 июня 1907 г._\n\r\n\rБот генерирует тексты на основе дневников и писем Л. Н. Толстого (и нескольких других источников). А настоящие цитаты из его дневников публикуются на странице «Лев Толстой. Секрет успеха». Им принадлежит фотография профиля бота.\n\r\n\rЕсли что-то идёт не так, напишите создательнице бота @murvn", parse_mode="Markdown", reply_markup=keyboard)

#отвечаем на все остальные сообщения, добавляем кнопку
@bot.message_handler(func=lambda m: True)
def send_letter(message):
    mess = markov_mess()
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Что нового, Лев Николаевич?')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, mess, reply_markup=keyboard)

@app.route("/", methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)