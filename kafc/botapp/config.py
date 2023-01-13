import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URI = os.getenv("DATABASE_URI")
WEBHOOK_HOST = '1ba3-178-133-216-61.eu.ngrok.io'
WEBHOOK_PORT = 443
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/webhook/%s/" % (BOT_TOKEN)