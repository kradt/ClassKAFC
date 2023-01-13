from kafc.botapp import bot
from kafc import create_app

app = create_app()
if __name__ == '__main__':
	bot.remove_webhook()

	try:
		bot.polling()
	except Exception:
		bot.polling()
