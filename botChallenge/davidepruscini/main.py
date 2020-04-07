# -*- coding: utf-8 -*-
"""
Bot Challenge - Main
Author: prushh
"""
import logging
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def quest0(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Quest0 command")


def quest1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Quest1 command")


def quest2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Quest2 command")


def status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Status command")


def unblocks(update, context):
    msg = update.message.text
    if msg == "giuro solennemente di non avere buone intenzioni":
        # TODO Add ConversationHandler with Quest 0, Quest 1, Quest 2
        print("Good passphrase!")
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="I don't have anything to say...")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Not valid command...")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token="TOKEN", use_context=True)

    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    bot_username = updater.bot.get_me()['username']
    print(f"{now} Authorized on account {bot_username}")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('quest0', quest0))
    dp.add_handler(CommandHandler('quest1', quest1))
    dp.add_handler(CommandHandler('quest2', quest2))

    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(MessageHandler(Filters.text, unblocks))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

    return 0


if __name__ == '__main__':
    exit(main())