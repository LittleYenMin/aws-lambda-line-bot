from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import json
import logging
import os
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

line_bot_api = LineBotApi(os.getenv('ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('SECRET'))


def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    try:
        # get X-Line-Signature header value
        signature = event['headers']['X-Line-Signature']
        # get event body
        body = event['body']
        # handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {'statusCode': 400, 'body': 'InvalidSignature'}
    except Exception as e:
        return {'statusCode': 400, 'body': json.dump(e)}
    return {'statusCode': 200, 'body': 'OK'}