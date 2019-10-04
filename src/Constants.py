import os


class Constants:
    SECRET_TOKEN = os.environ['CHANNEL_SECRET']
    ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
    DB_HOST = os.environ['DATABASE_HOST']
    DB_PORT = os.environ['DATABASE_PORT']
    DB = os.environ['DATABASE']
    DB_USER = os.environ['DATABASE_USER']
    DB_PASS = os.environ['DATABASE_PASS']
