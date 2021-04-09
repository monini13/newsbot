from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, replymarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import economist
import harvardbusiness
import reuters
import time
from urllib.parse import quote
from datetime import datetime
import copy
import numpy as np
import requests


news_url_dic = dict()
news_url_dic["economist"] = economist.get_economist_news
news_url_dic["hbr"] = harvardbusiness.get_hbr_news
news_url_dic["reuters"] = reuters.get_reuters_news

def start(update: Update, _: CallbackContext) -> None:
    reply_keyboard = [["/Economist"],["/HarvardBusinessReview"],["/Reuters"]]
    update.message.reply_text("Which news source would you like to view?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return None

def get_news_list(title_dic):
    to_view = "Which article would you like to view?\n\n"
    for idx in range(len(title_dic)):
        to_view += "{}) {}\n".format(idx,title_dic[idx])
    to_view += "\nOr send /start to view news catalog again"
    reply_keyboard = list()
    l = np.array(range(len(title_dic)))
    for row in np.array_split(l,3):
        reply_keyboard.append([ int(i) for i in row ])
    return to_view, reply_keyboard

def economist_command(update: Update, context: CallbackContext) -> None:
    if (datetime.utcnow()-context.bot_data['x']["timestamp"]).total_seconds() > 43200:
        update.message.reply_text("Please wait while we receive the latest news.")
        dispatcher_dic = add_news_sources()
        context.bot_data['x'] = dispatcher_dic.copy()
    handle = "economist"
    context.user_data['state'] = handle
    title_dic = context.bot_data['x'][handle]['title']
    to_view, reply_keyboard = get_news_list(title_dic)
    context.user_data['keyboard'] = reply_keyboard.copy()
    update.message.reply_text(to_view,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return None

def hbr_command(update: Update, context: CallbackContext) -> None:
    if (datetime.utcnow()-context.bot_data['x']["timestamp"]).total_seconds() > 43200:
        update.message.reply_text("Please wait while we receive the latest news.")
        dispatcher_dic = add_news_sources()
        context.bot_data['x'] = dispatcher_dic.copy()
    handle = "hbr"
    context.user_data['state'] = handle
    title_dic = context.bot_data['x'][handle]['title']
    to_view, reply_keyboard = get_news_list(title_dic)
    context.user_data['keyboard'] = reply_keyboard.copy()
    update.message.reply_text(to_view,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return None

def reuters_command(update: Update, context: CallbackContext) -> None:
    if (datetime.utcnow()-context.bot_data['x']["timestamp"]).total_seconds() > 43200:
        update.message.reply_text("Please wait while we receive the latest news.")
        dispatcher_dic = add_news_sources()
        context.bot_data['x'] = dispatcher_dic.copy()
    handle = "reuters"
    context.user_data['state'] = handle
    title_dic = context.bot_data['x'][handle]['title']
    to_view, reply_keyboard = get_news_list(title_dic)
    context.user_data['keyboard'] = reply_keyboard.copy()
    update.message.reply_text(to_view,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return None


def echo(update: Update, context: CallbackContext) -> None:
    article_number = 1e8
    user_input = update.message.text
    if user_input.isnumeric():
        article_number = int(float(user_input))
        handle = context.user_data['state']
        if article_number < len(context.bot_data['x'][handle]['news']):
            to_view_ls = context.bot_data['x'][handle]['news'][article_number]
            bot = context.bot
            for to_view in to_view_ls:
                bot.send_message(update.effective_chat.id, to_view)
            to_view = "Send /start to view news catalog again"
            update.message.reply_text(to_view,reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text(
                "Your input value is too large.",
                reply_markup=ReplyKeyboardMarkup(
                    context.user_data['keyboard'],
                    one_time_keyboard=True)
                )
    else:
        update.message.reply_text(
                "Unable to understand your input.",
                reply_markup=ReplyKeyboardMarkup(
                    context.user_data['keyboard'],
                    one_time_keyboard=True)
                )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')
    return None

def add_news_source(dispatcher_dic, handle, headline_func):
    dispatcher_dic[handle] = dict()
    dispatcher_dic[handle]['news'] = dict()
    temp_url_dic, temp_title_dic = headline_func()
    get_news_func = news_url_dic[handle]
    for key in temp_url_dic:
        print(temp_url_dic[key])
        page = requests.get(temp_url_dic[key])
        dispatcher_dic[handle]['news'][key] = get_news_func(page)
    dispatcher_dic[handle]['title'] = temp_title_dic.copy()
    return None

def add_news_sources():
    dispatcher_dic = dict()
    dispatcher_dic["timestamp"] = datetime.utcnow()
    add_news_source(dispatcher_dic,"economist",economist.get_headlines)
    add_news_source(dispatcher_dic,"hbr",harvardbusiness.get_headlines)
    add_news_source(dispatcher_dic,"reuters",reuters.get_headlines)
    print(datetime.now(),"News have been loaded")
    return dispatcher_dic

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher_dic = add_news_sources()
    dispatcher.bot_data["x"] = dispatcher_dic.copy()
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("Economist", economist_command))
    dispatcher.add_handler(CommandHandler("HarvardBusinessReview", hbr_command))
    dispatcher.add_handler(CommandHandler("Reuters", reuters_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    return None

if __name__ == "__main__":
    main()