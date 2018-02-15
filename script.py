import telebot
import cherrypy
import os
token='510800243:AAEsmyadUWf8h6VL4YV0HbjXtvuYVLRNpFQ'
WEBHOOK_HOST = 'https://zhankin-test3.herokuapp.com'
WEBHOOK_PORT = int(os.environ.get('PORT'))
WEBHOOK_LISTEN = '0.0.0.0'
#WEBHOOK_SSL_CERT = './webhook_cert.pem'
#WEBHOOK_SSL_PRIV = './webhook_pkey.pem'
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)

bot = telebot.TeleBot(token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()
#bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                certificate=open(WEBHOOK_SSL_CERT, 'r'))


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT
})



cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
