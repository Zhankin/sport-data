import logging
import os
import apidata
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update):
    update.effective_message.reply_text("Hi!")

def go(bot, update):
    update.effective_message.reply_text("go!")
def league(bot, update):
    
    update.effective_message.reply_text(apidata.getallleague())
def echo(bot, update):
    if update.effective_message.text[0]=='!':
        update.effective_message.reply_text(apidata.allcomands(update.effective_message.text[1:]))
    else:
	txt=update.effective_message.text
	txt=txt.split("%")
	output=apidata.mainfunc(txt[0],txt[1],txt[2])
	#print str(message.chat.id)
	#bot.send_message(message.chat.id,output)
	update.effective_message.send_photo('test.png')
                
	#bot.send_photo(message.chat.id,photo=open('test.png','rb'))

        #except:
	#continue
	#update.effective_message.reply_text('Ola-la')
            
def error(bot, update, error):
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
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('go', go))
    dp.add_handler(CommandHandler('league', league))
    dp.add_handler(MessageHandler(Filters.text, echo))
    #dp.add_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
