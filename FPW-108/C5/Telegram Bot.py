import telebot

TOKEN = "6178151805:AAG26wHDEEvVMhIi573SxDFUVSX4h0a2c7I"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['text'])
def send_hello(message):
    bot.send_message(message.chat.id, 'This is just testing')


bot.polling()