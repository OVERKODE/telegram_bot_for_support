import telebot # import essential libraries.

API = 'YOUR_API_TOKEN' # API from @BotFather.
ADMIN = 0 # Admin's ID.

bot = telebot.TeleBot(API) # Initializing bot as an object in programm.

@bot.message_handler(commands=['start']) # Basic start func. If user is admin, bot will offer him to answer a message, If not, bot will offer to ask a question.
def start(message):
    if message.from_user.id != ADMIN:
        bot.send_message(message.from_user.id, "👋 Hello and welcome! Here you can ask your question. Use the command /ask_question")
    else:
        bot.send_message(ADMIN, "Hello! To reply to a message, use the /reply command")

@bot.message_handler(commands=['ask_question']) # Bot's answer on "/ask_question" command.
def user_send_msg(message):
    bot.send_message(message.from_user.id, "Write your question below:")
    bot.register_next_step_handler(message, bot_send_msg)

def bot_send_msg(message): # Here bot sends a message to admin.
    msg = message.text
    try:
        bot.send_message(ADMIN, f"📨 New message from user @{message.from_user.username} (ID: {message.from_user.id})!\n\n{msg}")
        bot.send_message(message.from_user.id, "✅ Successfully sent!")
    except Exception as e:
        bot.send_message(message.from_user.id, "❌ An error occurred! Try again.")

@bot.message_handler(commands=['reply']) # Bot's answer on "/reply" command. Here bot asks for user's ID.
def reply(message):
    if message.from_user.id == ADMIN:
        bot.send_message(ADMIN, "Enter the ID of the user whose message you want to reply to:")
        bot.register_next_step_handler(message, bot_catch_id)
    else:
        bot.send_message(message.from_user.id, "❌ Not enough rights!")

def bot_catch_id(message): # Here bot catches user's ID and asks for the message for user.
    user_id = message.text
    bot.send_message(ADMIN, "Now enter a message for him:")
    bot.register_next_step_handler(message, lambda m: bot_catch_and_send_msg(m, user_id))

def bot_catch_and_send_msg(message, user_id): # Here bot catches message and send it for user whose ID admin wrote in previous function.
    msg = message.text
    try:
        bot.send_message(user_id, f"📨 The answer has arrived!\n\n{msg}")
        bot.send_message(ADMIN, "✅ Successfully sent!")
    except:
        bot.send_message(ADMIN, "❌ An error occurred! Try again.")

bot.polling() # Initializing bot in Telegram.

