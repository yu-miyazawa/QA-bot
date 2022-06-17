from flask import Flask,request,abort,render_template, jsonify
from app import answer
import os


from linebot import (
    LineBotApi,WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent,TextMessage,TextSendMessage,
)


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

    #返信文のテキスト処理
    #reply_message = mining(event.message.text)
    data = answer(event.message.text)
    reply_message = '最も関連度の高い回答はこちらです。\n\n' + '【質問】\n' + data['hit_question']+'\n\n' + '【回答】\n' + data['hit_answer']

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    app.run(debug=True)
