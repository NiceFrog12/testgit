import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для успокаивания непослушных детей.")


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Не прыгай выше головы)")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Непослушный ребенок @{message.reply_to_message.from_user.username} был наказан.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(commands=['convert'])
def convertcurrency(message):
    money = {"USD" : 0.011, "EUR" : 0.0097, "JPY" : 1.56}
    currency = ", ".join(money.keys())
    answer = f"Поддерживаемые валюты на данный момент только: {currency} (сравнивает всё с рублем) \nкомманда выглядит так: /convert [кол-во] (валюта)"
    msg = message.text.split(" ")


    try:
        amount = float(msg[1])
        postconvert = msg[2]
    except:
        bot.reply_to(message, answer)

    try:
        endresult = amount * money[postconvert]
        bot.reply_to(message, f"{amount} рублей в {postconvert} это {endresult:.2f}")
    except TypeError as e:
        bot.reply_to(message, "кол-во должно быть дано в цифрах")
        
    except KeyError:
        bot.reply_to(message, f"Данная валюта не поддерживается. \nПопробуйте что-то из этого: {currency}")
    


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text.startswith("https://"):
        chat_id = message.chat.id
        user_id = message.from_user.id
        bot.ban_chat_member(chat_id, user_id)
    else:
        bot.reply_to(message, message.text) 


bot.infinity_polling(none_stop=True)
