import os
import sys
import threading
import time

import requests
from flask import Flask, abort, request

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from src.Routing.Callback import Callback
from src.Routing.Root import Root

app = Flask(__name__)

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.environ['CHANNEL_SECRET']
channel_access_token = os.environ['CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 多分ここら原因
host = "0.0.0.0"
port = int(os.environ.get("PORT", 5000))


@app.route("/")
def hello_world():
    return Root.ret()


@app.route("/callback", methods=['POST'])
def callback():
    return Callback.ret()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


def check():
    while True:
        time.sleep(60 * 10)
        requests.get(host + '/check')


if __name__ == "__main__":
    app.run(host=host, port=port)
    threading.Thread(target=check,).start()
