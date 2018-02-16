import os
import logging
import apidata
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

CHOOSING_LEAGUE, TYPING_REPLY_1TEAM = range(2)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
	reply_keyboard = apidata.getallleague_ls()
	markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
	update.message.reply_text("Choose your destiny!",reply_markup=markup)
	
	return CHOOSING_LEAGUE

def teams_list(bot, update,user_data):
	text = update.message.text
	user_data['choice'] = text
	
	reply_keyboard = apidata.allcomands_ls(text)
	markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
	update.message.reply_text("Choose your destiny!",reply_markup=markup)
	
	return TYPING_REPLY_1TEAM

def team2_choise(bot, update, user_data):
    update.message.reply_text("okok")
    user_data.clear()
    return ConversationHandler.END

def done(bot, update, user_data):
    update.message.reply_text("Bye")
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    
    
    
    
if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "510800243:AAEsmyadUWf8h6VL4YV0HbjXtvuYVLRNpFQ"
    NAME = "zhankin-sports-data"

    # Port is given by Heroku
    PORT = int(os.environ.get('PORT'))

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING_LEAGUE: [MessageHandler(Filters.text,
                                          teams_list,
                                          pass_user_data=True),
                           ],

            TYPING_REPLY_1TEAM: [MessageHandler(Filters.text,
                                           team2_choise,
                                           pass_user_data=True),
                            ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    #dp.add_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
