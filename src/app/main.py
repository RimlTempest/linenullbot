import json
import os
import random
import sys
import threading

from flask import Flask
from jinja2 import Environment, FileSystemLoader, select_autoescape
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, QuickReplyButton, MessageAction, QuickReply, FlexSendMessage, BubbleContainer, ImageComponent,
    URIAction, CarouselContainer)

from src.Cmds import Janken
from src.Decorators.ErrorDecorator import Err_tag
from src.Constants import Constants
from src.Routing import Root
from src.Routing import Callback
from src.Utils import LoginChecker
from src.Utils.HerokuChecker import check

#  app call
app = Flask(__name__)
#  Token check
LoginChecker.check(Constants.SECRET_TOKEN, Constants.ACCESS_TOKEN)
# 　Client handler generation
client = LineBotApi(Constants.ACCESS_TOKEN)
handler = WebhookHandler(Constants.SECRET_TOKEN)
# 　load in flexMessage
template_env = Environment(
    loader=FileSystemLoader('src/View'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)

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
    hands = ["グー", "チョキ", "パー"]

    if event.message.text == 'じゃんけん':
        hands_img = {"グー":"https://image.middle-edge.jp/medium/d334db3f-010d-45f0-8999-d57c84e76677.jpg?1485589415",
                     "チョキ":"https://www.sozai-library.com/wp-content/uploads/2015/07/5092-300x225.jpg",
                     "パー":"https://image.jimcdn.com/app/cms/image/transf/none/path/se516d3bb2a89d52e/image"
                     "/i65b87465dfb3a4ab/version/1551120498/image.jpg"
                     }
        items = [QuickReplyButton(image_url=hands_img[hand],
                                  action=MessageAction(
                                      label=f"{hand}",
                                      text=f"{hand}")
                                  ) for hand in hands]
        messages = TextSendMessage(text="じゃーんけーん", quick_reply=QuickReply(items=items))
        client.reply_message(event.reply_token, messages=messages)
    elif event.message.text in hands:
        client.reply_message(event.reply_token, TextSendMessage(Janken.Rock_Paper_Scissors(event.message.text)))

    if event.message.text == 'help':
        client.reply_message(event.reply_token, TextSendMessage("Send -> じゃんけん\nSend -> bye\nSend -> Test"))

    if event.message.text == "bye":
        client.reply_message(event.reply_token, TextSendMessage("See you!"))

        # グループトークからの退出処理
        if hasattr(event.source, "group_id"):
            client.leave_group(event.source.group_id)

        # ルームからの退出処理
        if hasattr(event.source, "room_id"):
            client.leave_room(event.source.room_id)

        return

    if event.message.text == "dir":
        currentdir = os.getcwd()
        ls = os.listdir(currentdir)
        full_path = os.path.realpath(__file__)
        client.reply_message(event.reply_token, TextSendMessage(str(
            f"{currentdir}\n{str(ls)}\n{full_path}")))

    if event.message.text == "Test":
        try:
            item = "ぶりぶり"
            template = template_env.get_template('Test.json')
            data = template.render(dict(items=item))
            client.reply_message(event.reply_token,
                                 messages=FlexSendMessage(
                                     alt_text='hello',
                                     contents=CarouselContainer.new_from_json_dict(json.loads(data))))
        except Exception as e:
            tb = sys.exc_info()[2]
            client.reply_message(event.reply_token, TextSendMessage(f"[Error]\nType:{str(type(e))}\n"
                                                                    f"Args:{str(e.args)}\n"
                                                                    f"Except:{str(e)}\n"
                                                                    f"Mes:\n{e.with_traceback(tb)}"))

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
