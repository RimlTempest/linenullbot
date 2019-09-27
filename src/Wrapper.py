from linebot.models import TextSendMessage, QuickReplyButton, MessageAction, QuickReply


class Client:
    def __init__(self, client, event):
        self.client = client
        self.event = event

    @staticmethod
    def sendText(self, text):
        return self.client.reply_message(self.event.reply_token,
                                         TextSendMessage(text=text))

    @staticmethod
    def sendCarousel(self, list, text):
        items = [QuickReplyButton(action=MessageAction(label=f"{day}", text=f"{day}")) for day in list]
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
        return self.client.reply_message(self.event.reply_token, messages=messages)
