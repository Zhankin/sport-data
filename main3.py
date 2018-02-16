import os
import logging
import apidata
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

CHOOSING_LEAGUE,CHOOSING_HOME_TEAM, CHOOSING_AWAY_TEAM, FINAL = range(4)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
	try:
		reply_keyboard = apidata.getallleague_ls()
		markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
		update.message.reply_text("Choose your destiny!",reply_markup=markup)
		return CHOOSING_HOME_TEAM
	except:
		update.message.reply_text("Please try again from /start")
		return FINAL

def team_home(bot, update,user_data):
	try:
		text = update.message.text
		user_data['league'] = text

		reply_keyboard = apidata.allcomands_ls(text)
		markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
		update.message.reply_text("Choose home team!",reply_markup=markup)

		return CHOOSING_AWAY_TEAM
	except:
		update.message.reply_text("wow wow something broken try again from /start")
		return FINAL



def team_away(bot, update, user_data):
	try:
		text = update.message.text
		if text!='Back to main menu':
			user_data['team_home'] = text

			reply_keyboard = apidata.allcomands_ls(user_data['league'])
			markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
			update.message.reply_text("Choose away team!",reply_markup=markup)


			return FINAL
		else:
			return CHOOSING_LEAGUE
	except:
		update.message.reply_text("pfff something broken try again from /start")
		return CHOOSING_LEAGUE
		

def final_message(bot, update, user_data):
	try:
		text = update.message.text
		if text!='Back to main menu':
			user_data['team_away'] = text

			output=apidata.mainfunc(user_data['team_home'],user_data['team_away'],user_data['league'])
			update.effective_message.reply_photo(photo=open('test.png','rb'))
			user_data.clear()
			return ConversationHandler.END
		else:
			return CHOOSING_LEAGUE
	except:
		user_data.clear()
		update.message.reply_text("bye-bye")
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
                                          start),
                           ],
            CHOOSING_HOME_TEAM: [MessageHandler(Filters.text,
                                          team_home,
                                          pass_user_data=True),
                           ],

            CHOOSING_AWAY_TEAM: [MessageHandler(Filters.text,
                                           team_away,
                                           pass_user_data=True),
                            ],
            FINAL: [MessageHandler(Filters.text,
                                           final_message,
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
