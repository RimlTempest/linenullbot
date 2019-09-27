import os


class Constants:
    SECRET_TOKEN = os.environ['CHANNEL_SECRET']
    ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
