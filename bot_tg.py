import telebot
from telebot import types
import requests

bot = telebot.TeleBot("5242451797:AAGn75528zlVyI0aznFsAdAhktffBbAFGdU")


@bot.message_handler(commands=["start"])
def start_bot(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать погоду")
    markup.add(item1)
    bot.send_message(message.chat.id, "Бот запущен", reply_markup=markup,
                     parse_mode="MARKDOWN")


@bot.message_handler(content_types=['text'])
def check(message):
    if message.text == "Узнать погоду":
        bot.send_message(message.chat.id, "Введите город")
        bot.register_next_step_handler(message, weather)


def weather(message):
    try:
        city = message.text
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=c68da8c66b65f3680f66d29eea8406fe&units=metric")
        data = r.json()

        city = data["name"]
        temp = data["main"]["temp"]

        markup_inline = types.InlineKeyboardMarkup()
        item_good = types.InlineKeyboardButton(text="Отлично", callback_data='good')
        item_bad = types.InlineKeyboardButton(text="Плохо", callback_data='bad')
        markup_inline.add(item_good, item_bad)

        bot.send_message(message.chat.id, f"В городе {city}, температура {temp}", reply_markup=markup_inline)

    except KeyError:
        bot.send_message(message.chat.id, "Такого города нет")


@bot.callback_query_handler(func=lambda call: True)
def answer(call: telebot.types.CallbackQuery):
    if call.data == 'good':
        bot.edit_message_text(f"{call.message.text}\n\n"
                              f"_Сегодня отличная погода_", call.message.chat.id, call.message.id,
                              parse_mode="MARKDOWN")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    elif call.data == 'bad':
        bot.edit_message_text(f"{call.message.text}\n\n"
                              f"_Погода плохая, можно остаться дома_", call.message.chat.id, call.message.id,
                              parse_mode="MARKDOWN")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
