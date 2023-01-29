import telebot
import logging
from logging.handlers import RotatingFileHandler
from core.data import TOKEN
from telegram.schedule.data import TEXT_BUTTON_NOW, TEXT_BUTTON_DAY, TEXT_BUTTON_WEEK

bot = telebot.TeleBot(token=TOKEN)


main_markup = telebot.types.ReplyKeyboardMarkup(True)
main_markup.add(TEXT_BUTTON_NOW, TEXT_BUTTON_DAY, TEXT_BUTTON_WEEK)

# log configuration
logger = logging.getLogger(data.LOG_NAME)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(data.LOG_FILE_NAME, maxBytes=data.LOG_MAX_SIZE_BYTES, 
backupCount=data.LOG_BACKUP_COUNT)
handler.setFormatter(logging.Formatter(data.LOG_MESSAGE_FORMAT, data.LOG_DATE_FORMAT))
logger.addHandler(handler)


def log(module, message):
    if message.from_user.username:
        user = message.from_user.username
    else:
        user = str(message.from_user.id)
    logger.info(f"{module.rjust(15)} :: {user.rjust(20)} ::"
    f"{message.text if message.text else '--not_text--'}")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hey Daniel Here")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print(message)
    bot.reply_to(message, message.text)

