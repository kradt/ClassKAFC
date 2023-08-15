import os
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


def get_ngrok_public_address():
    try:
        response = requests.get("http://host.docker.internal:4040/api/tunnels")
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print("Error fetching Ngrok public address:", e)
        return None


class Config:
	DEBUG = True
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
	BUCKET_NAME = os.getenv("BUCKET_NAME")
	BOT_TOKEN = os.getenv("BOT_TOKEN")
	WEBHOOK_URL_PATH = "/webhook/{}/".format(BOT_TOKEN) 
	WEBHOOK_URL_BASE = get_ngrok_public_address()
	DATABASE_URI = os.getenv("DATABASE_URL")
	AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
	AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
	CELERY = {
        "broker_url": os.getenv("REDIS_URL"),
        "result_backend": os.getenv("REDIS_URL")
    }
