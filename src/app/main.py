import os
import sys
import threading

from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, QuickReplyButton, MessageAction, QuickReply)

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
    if event.message.text == '時間割を教えて':
        day_list = ["月", "火", "水", "木", "金"]
        items = [QuickReplyButton(action=MessageAction(label=f"{day}", text=f"{day}曜日の時間割")) for day in day_list]
        messages = TextSendMessage(text="何曜日の時間割ですか？", quick_reply=QuickReply(items=items))
        client.reply_message(event.reply_token, messages=messages)
    '''client.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))'''

# フォローイベントの場合の処理
@handler.add(FollowEvent)
def handle_follow(event):
    client.reply_message(
        event.reply_token,
        TextSendMessage(text='Follow, thank you for unblocking! Nice to meet you!')
    )


#  main
if __name__ == "__main__":
    app.run(host=Constants.HOST, port=Constants.PORT)
    threading.Thread(target=check, ).start()
