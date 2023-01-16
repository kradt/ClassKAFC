import os

class Config:
	DEBUG = True
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
	BUCKET_NAME = os.getenv("BUCKET_NAME")
	AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
	AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")

	