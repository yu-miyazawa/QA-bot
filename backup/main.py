from flask import Flask,request,abort

from linebot import (
    LineBotApi,WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent,TextMessage,TextSendMessage,
)

import os

#返信用の自作関数を呼び出し
from learning import rpy_message
from text_mining import mining

app = Flask(__name__)

# アクセストークン取得
line_bot_api = LineBotApi("A3hHLDTYZQn/B45onfS1n8lbkAZNc9TlFHmSE1S5BBopoyV3VmI71YgG7WrQOq734S9B9r1PA5mrxMv3k6tiatLjvINLYxHZlSc0yOtWz5x9/LySATgCykyX8ADUkksMO0gZ8fmx//hT6iekTvCb6wdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("759f9e93d59f1ec73282d53b066a2ec6")


@app.route("/")
def test():
    return"OK!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #reply_message = rpy_message(event.message.text)
    reply_message = mining(event.message.text)

    # #「こんにちは」と来た場合の返事
    # if event.message.text == "こんにちは":
    #     reply_message = "こんにちは。\nいい天気ですね。"
    
    # #「好きな食べ物は？」と来た場合の返事
    # elif event.message.text == "好きな食べ物は？":
    #     reply_message = "餃子、ハンバーグ、オムライス等々"
    
    # elif event.message.text =="はまち" or "はまち！" or "ハマチ" or "ハマチ！":
    #     reply_message = "三種の神器の一つ。\nちゃいろの毛玉。\nもふもふかわいい...。"

    # #それ以外の返事
    # else:
    #     reply_message = f"あなたは「{event.message.text}」と言いました！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    app.run(debug=True)