# -*- coding: utf-8 -*-
"""
Bot Challenge - Mime of Engine
Author: prushh
"""
import logging
from datetime import datetime

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from settings import TOKEN, passphrase, endphrase
from quests import create_qts, check_choice, check_qts, get_solved, NUM_QTS

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def quest0(update, context):
    '''Command for quest0.'''
    reply = check_qts(context, 0)
    update.message.reply_text(reply)


def quest1(update, context):
    '''Command for quest1.'''
    reply = check_qts(context, 1)
    update.message.reply_text(reply)


def quest2(update, context):
    '''Command for quest2.'''
    reply = check_qts(context, 2)
    update.message.reply_text(reply)


def status(update, context):
    '''Show number of completed quests.'''
    if 'quests' in context.user_data.keys():
        quests = context.user_data['quests']
        solved_qts = get_solved(quests)
        reply = f"Hai completato {solved_qts} quest su {NUM_QTS}"
    else:
        reply = f"Hai completato 0 quest su {NUM_QTS}"
    update.message.reply_text(reply)


def unknown(update, context):
    '''Reply to all unrecognized commands.'''
    update.message.reply_text("Comando non valido...")


def cancel(update, context):
    print("Cancel command")
    return ConversationHandler.END


def error(update, error):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, error)


def quest_choice(update, context):
    '''
    Bot core to interact with quests.
    '''
    msg = update.message.text.lower()
    quests = context.user_data['quests']

    if msg == endphrase:
        if get_solved(quests) == NUM_QTS:
            reply = "Congratulazioni! Hai finito tutte le missioni..."
            reply_markup = ReplyKeyboardRemove()
            update.message.reply_text(reply, reply_markup=reply_markup)
            return ConversationHandler.END
        reply = "Non hai completato tutte le missioni. Che peccato..."
    elif msg == 'quest 0':
        reply = check_choice(quests, 0)
    elif msg == 'quest 1':
        reply = check_choice(quests, 1)
    elif msg == 'quest 2':
        reply = check_choice(quests, 2)
    else:
        reply = "Non ho niente da dire..."

    update.message.reply_text(reply)


def unlocks(update, context):
    '''
    Unlock missions with the correct passphrase
    '''
    msg = update.message.text.lower()
    reply = "Non ho niente da dire..."

    if msg == passphrase:
        if 'quests' not in context.user_data.keys():
            # Differenza: lui crea quests al primo msg senza passphrase
            context.user_data['quests'] = create_qts()
        reply_keyboard = [['Quest 0', 'Quest 1', 'Quest 2']]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(reply, reply_markup=markup)
        return 1
    elif msg == endphrase:
        if 'quests' in context.user_data.keys():
            quests = context.user_data['quests']
            if get_solved(quests) == NUM_QTS:
                reply = "Congratulazioni! Hai finito tutte le missioni..."
        else:
            reply = "Non hai completato tutte le missioni. Che peccato..."

    update.message.reply_text(reply)
    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Display authorization message
    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    bot_username = updater.bot.get_me()['username']
    print(f"{now} Authorized on account {bot_username}")

    # Adding all the handler for the commands
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('quest0', quest0))
    dp.add_handler(CommandHandler('quest1', quest1))
    dp.add_handler(CommandHandler('quest2', quest2))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    cmd_unlocks = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, unlocks)],

        states={
            1: [MessageHandler(
                    Filters.regex('^(Quest 0|Quest 1|Quest 2)$'),
                    quest_choice),
                MessageHandler(Filters.text, quest_choice)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(cmd_unlocks)

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

    return 0


if __name__ == '__main__':
    exit(main())
