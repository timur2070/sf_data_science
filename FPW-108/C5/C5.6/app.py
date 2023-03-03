import telebot
from config import TOKEN, KEYS
from extensions import CurrencyConverter, ConversionError

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_commands(message):
    bot.send_message(message.chat.id, 'Welcome to the currency converter bot!\n\
To convert currency type in the following format:\n\
<from currency> <to currency> <amount to convert>.\n\
For the list of available currencies type /values')

@bot.message_handler(commands=['values'])
def values(message):
    text = 'The list of available currencies for conversion:'
    for key in KEYS:
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message):
    try:
         input = message.text.split(' ')

         if len(input) != 3:
             raise ConversionError('Wrong number of arguments. Check your input')
         base, quote, amount = input
         result = CurrencyConverter.get_price(base, quote, amount)
    except ConversionError as e:
        bot.reply_to(message, f'User input error:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Couldnt process the command:\n{e}')
    else:
        text = f'The current rate:\n{amount} {base} is equal {result} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()