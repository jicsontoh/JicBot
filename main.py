import os
import http
import random

import pymongo
from flask import Flask, request
from werkzeug.wrappers import Response


from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, Filters, MessageHandler, CallbackContext, CommandHandler, Updater

app = Flask(__name__)


client = pymongo.MongoClient(os.environ["MongoDB"])
db = client.test


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
    db.test.insert_one({"name": update.message.text})


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello! I am JicBot. How can I help you :)")


def help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Here are the available commands: \n"
                                                   "/start\n"
                                                   "/help")
def decide(update, context):
    chat_id = update.effective_chat.id
    rand = random.randint(0, len(context.args) - 1)
    res = "Hmmm we will go with "
    res += context.args[rand]
    context.bot.send_message(chat_id=chat_id, text=res)

def test(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="This is testing locally")


bot = Bot(token=os.environ["TOKEN"])

updater = Updater(token=os.environ["TOKEN"], use_context=True)
dispatcher = updater.dispatcher

# dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("test", test))
dispatcher.add_handler(CommandHandler("decide", decide))

# to test locally
# updater.start_polling()

@app.post("/")
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
