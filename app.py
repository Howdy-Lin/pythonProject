# -*- coding:utf-8-*-

import requests
from datetime import datetime

from flask import Flask, request, abort
import json, time
import pandas as pd

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from file import File
from ai import predict_image_with_path
from solve_cudnn_error import *
import subprocess
import os
import  pyimgur
solve_cudnn_error()
# Channel Access Token
file = open('channel_access_token.txt', encoding='utf8')
text = file.read().strip()
line_bot_api = LineBotApi(text)
file.close()

# Channel Secret
file = open('channel_secret.txt', encoding='utf8')
text = file.read().strip()
handler = WebhookHandler(text)
file.close()

app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi('nFwEsfLdIC6alMzF0TyZ36YHP5wAMKcWL7d4/YOBLwKaWEDzT7kbymhln7M60HkktRHmG6mBCpFlbC9XoH+UfwEw5Dwy6ZRaZXSa/RHSryZc85TiOAQhgv5GH0Afigh7jHMebVZTFOKPbrU2da6woAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('cf812ba0afa3b21f819d8fbba0dcf47f')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'
'''
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def index():
    return 'Hello World'
'''
# 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    is_image = False
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        is_image = True
    else:
        return    
    response_text='衛生紙'
    if is_image == True:
       #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response_text))
       message_content = line_bot_api.get_message_content(event.message.id)
       img, path1 = file.save_bytes_image(message_content.content)

       user_profile = line_bot_api.get_profile(event.source.user_id)
       IDKEY = str(user_profile.user_id)

       line_bot_api.push_message( IDKEY, TextSendMessage(text='請稍等  圖片辨識中....'))

       print(path1)
       pred = predict_image_with_path(path1)
       print(pred)
       pred=str(pred)

       line_bot_api.reply_message(event.reply_token, TextSendMessage(text=pred))

       if '不是' in pred:          #辨識結果若為衛生紙  則回傳購物網站
           pass
       else:
           line_bot_api.push_message(IDKEY, TextSendMessage(text='https://emart0317.herokuapp.com/result'))
       '''
       count=0
       os.system("python detect.py --weights tissue_yolov5l.pt --img 640 --conf 0.7 --source ./media/user_sent.jpg --save-txt --save-crop")
       image_message =ImageSendMessage('')
       path = './runs/detect'
       for fn in os.listdir(path):     #數資料夾內數量  計算exp()
           count += 1
       path2 = f'./runs/detect/exp{count}/crops'
       print(path2)

       if os.path.exists(path2) == True:
           message='是衛生紙'
       else:
           message='不是衛生紙'       
       CLIENT_ID = 'fe38e69802c6777'
       PATH = f"./runs/detect/exp{count}/user_sent.jpg"
       im = pyimgur.Imgur(CLIENT_ID)
       uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
       print(uploaded_image.link)

       image_message = ImageSendMessage(
           original_content_url=uploaded_image.link,
            preview_image_url = uploaded_image.link)
       line_bot_api.reply_message(event.reply_token, image_message)
       line_bot_api.push_message(IDKEY, TextSendMessage(text=message))
       '''
       #image_message =  ImageSendMessage(f'./runs/detect/runs/exp{count}/user_sent.jpg')
       #print(image_message)
       #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


file = File()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
