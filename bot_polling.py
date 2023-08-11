from kafc.botapp import bot
from kafc.botapp.view import *

# start bot in polling mode

if __name__ == '__main__':
	bot.remove_webhook()
	bot.polling()