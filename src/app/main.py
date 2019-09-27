import os
import sys
import threading

from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from src.Constants import Constants
from src.Routing import Root
from src.Routing import Callback
from src.Utils import LoginChecker
from src.Utils.HerokuChecker import check

#  app call
app = Flask(__name__)
#  Token check
LoginChecker.check(Constants.SECRET_TOKEN, Constants.ACCESS_TOKEN)
#  object gen
client = LineBotApi(Constants.ACCESS_TOKEN)
handler = WebhookHandler(Constants.SECRET_TOKEN)


#  routing
@app.route("/")
def hello_world():
    return Root.rootRet()


@app.route("/callback", methods=['POST'])
def callback():
    return Callback.callbackRet()


#  event handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    client.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


#  main
if __name__ == "__main__":
    app.run(host=Constants.HOST, port=Constants.PORT)
    threading.Thread(target=check, ).start()
