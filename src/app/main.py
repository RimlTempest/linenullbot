import os
import random
import sys
import threading

from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, QuickReplyButton, MessageAction, QuickReply, FlexSendMessage, BubbleContainer, ImageComponent,
    URIAction)

from src.Wrapper import Client
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
    # Wrap
    Client.client = client
    Client.event = event

    if event.message.text == 'じゃんけん':
        day_list = ["チョキ", "グー", "パー"]
        len_list = []
        text = ""
        botflg = random.randint(0, 2)
        items = [QuickReplyButton(action=MessageAction(label=f"{day}", text=f"{day}を出しました。")) for day in day_list]
        messages = TextSendMessage(text="じゃーんけーん", quick_reply=QuickReply(items=items))
        client.reply_message(event.reply_token, messages=messages)

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

    if event.message.text == "Test":
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                      "type": "carousel",
                      "contents": [
                        {
                          "type": "bubble",
                          "size": "micro",
                          "hero": {
                            "type": "image",
                            "url": "https://shiawaseninaritai.com/wp-content/uploads/2019/05/39f94af6e839a79ce57553873b282f7b-728x427.png",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "320:213"
                          },
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "ゆゆうた",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                              },
                              {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                  },
                                  {
                                    "type": "text",
                                    "text": "4.0",
                                    "size": "xs",
                                    "color": "#8c8c8c",
                                    "margin": "md",
                                    "flex": 0
                                  }
                                ]
                              },
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "OMMC",
                                        "wrap": True,
                                        "color": "#8c8c8c",
                                        "size": "xs",
                                        "flex": 5
                                      }
                                    ]
                                  }
                                ]
                              }
                            ],
                            "spacing": "sm",
                            "paddingAll": "13px"
                          }
                        },
                        {
                          "type": "bubble",
                          "size": "micro",
                          "hero": {
                            "type": "image",
                            "url": "https://livedoor.blogimg.jp/jin115/imgs/6/1/61d89d0f.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "320:213"
                          },
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "からさわたかひろ",
                                "weight": "bold",
                                "size": "sm",
                                "wrap": True
                              },
                              {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                  },
                                  {
                                    "type": "text",
                                    "text": "4.0",
                                    "size": "sm",
                                    "color": "#8c8c8c",
                                    "margin": "md",
                                    "flex": 0
                                  }
                                ]
                              },
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "あああああああ",
                                        "wrap": True,
                                        "color": "#8c8c8c",
                                        "size": "xs",
                                        "flex": 5
                                      }
                                    ]
                                  }
                                ]
                              }
                            ],
                            "spacing": "sm",
                            "paddingAll": "13px"
                          }
                        },
                        {
                          "type": "bubble",
                          "size": "micro",
                          "hero": {
                            "type": "image",
                            "url": "https://i.ytimg.com/vi/Mr5gPPYBlg8/maxresdefault.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "320:213"
                          },
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "しゃむ",
                                "weight": "bold",
                                "size": "sm"
                              },
                              {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "xs",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                  },
                                  {
                                    "type": "text",
                                    "text": "4.0",
                                    "size": "sm",
                                    "color": "#8c8c8c",
                                    "margin": "md",
                                    "flex": 0
                                  }
                                ]
                              },
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "それってYO！",
                                        "wrap": True,
                                        "color": "#8c8c8c",
                                        "size": "xs",
                                        "flex": 5
                                      }
                                    ]
                                  }
                                ]
                              }
                            ],
                            "spacing": "sm",
                            "paddingAll": "13px"
                          }
                        }
                      ]
                    }
        )
        client.reply_message(event.reply_token, messages=flex_message)
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
