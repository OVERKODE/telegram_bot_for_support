import telebot

API = '8398206535:AAGIUwRcqyYatJzcjRk8DH8BFn1-92D3afg'
ADMIN = 6586273953

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN:
        bot.send_message(message.from_user.id, "👋 Привет и добро пожаловать! Тут ты можешь задать свой вопрос. Воспользуйся командой /ask_question")
    else:
        bot.send_message(ADMIN, "Привет! Для ответа на сообщение используй команду /reply")

@bot.message_handler(commands=['ask_question'])
def user_send_msg(message):
    bot.send_message(message.from_user.id, "Напиши свой вопрос ниже:")
    bot.register_next_step_handler(message, bot_send_msg)

def bot_send_msg(message):
    msg = message.text
    try:
        bot.send_message(ADMIN, f"📨 Новое сообщение от пользователя @{message.from_user.username} (ID: {message.from_user.id})!\n\n{msg}")
        bot.send_message(message.from_user.id, "✅ Успешно отправлено!")
    except Exception as e:
        bot.send_message(message.from_user.id, "❌ Произошла ошибка! Попробуй заново.")

@bot.message_handler(commands=['reply'])
def reply(message):
    if message.from_user.id == ADMIN:
        bot.send_message(ADMIN, "Введи ID пользователя, на сообщение которого хочешь ответить:")
        bot.register_next_step_handler(message, bot_catch_id)
    else:
        bot.send_message(message.from_user.id, "❌ Недостаточно прав!")

def bot_catch_id(message):
    user_id = message.text
    bot.send_message(ADMIN, "Теперь введи сообщение для него:")
    bot.register_next_step_handler(message, lambda m: bot_catch_and_send_msg(m, user_id))

def bot_catch_and_send_msg(message, user_id):
    msg = message.text
    try:
        bot.send_message(user_id, f"📨 Пришел ответ!\n\n{msg}")
        bot.send_message(ADMIN, "✅ Успешно отправлено!")
    except:
        bot.send_message(ADMIN, "❌ Произошла ошибка! Попробуй заново.")

bot.polling()