# -*- coding: utf-8 -*-
import os
import random

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage
)

from line_auth_key import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase
from app.line_templates import make_template_action, make_carousel_column, make_carousel_template, make_confirm_template, make_buttons_template
from app import wtf_reasons
from app import cwb_weather_predictor

maple_phrase = horse_phrase + lion_phrase + dunkey_phrase


application = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@application.route('/')
def hello_world():
    return '<a href=\'https://github.com/leafwind/line_bot\'>https://github.com/leafwind/line_bot</a>'

@application.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    application.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('=========')
    print(event.__dict__)
    print(event.source.__dict__)
    leafwind_photo_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/panel-145336656-image-e9329cd5f8f44a76-320-320.png'
    kaori_photo_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/panel-145336656-image-4808e3743f50232e-320-320.jpeg'
    uri_action = make_template_action('uri', '前往卡歐的首頁', uri='http://yfting.com')
    uri_action2 = make_template_action('uri', '前往玉米的首頁', uri='https://data.leafwind.tw')
    postback_action = make_template_action('postback', 'ping', data='ping')
    postback_action_with_text = make_template_action('postback', 'ping with text', data='ping', text='ping')
    message_action = make_template_action('message', 'Translate Rice', text='米')
    if event.message.text == 'carousel':
        col1 = make_carousel_column('這是卡歐', 'Hi~', [uri_action, postback_action], kaori_photo_url)
        col2 = make_carousel_column('這是玉米', 'ㄏㄏ', [uri_action2, message_action], leafwind_photo_url)

        carousel_template = make_carousel_template([col1, col2])

        template_message = TemplateSendMessage(
            alt_text='carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.message.text == 'confirm':  # left / right buttons
        message_action = make_template_action('message', '是', text='帥！')
        message_action2 = make_template_action('message', '否', text='帥！')
        confirm_template = make_confirm_template('玉米帥嗎？', [message_action, message_action2])
        template_message = TemplateSendMessage(
            alt_text='confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.message.text == 'buttons':  # top-down buttons
        buttons_template = make_buttons_template(
            'My buttons sample',
            'Hello, my buttons',
            [uri_action, postback_action, postback_action_with_text, message_action],
            leafwind_photo_url
        )
        template_message = TemplateSendMessage(
            alt_text='buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.source.type == 'room':
        rid = event.source.room_id
        reply = make_reply('room', rid, event.message.text)
    elif event.source.type == 'user':
        uid = event.source.user_id
        reply = make_reply('user', uid, event.message.text)
    elif event.source.type == 'group':
        gid = event.source.group_id
        reply = make_reply('group', gid, event.message.text)

    if not reply:
        return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

def make_reply(type, uid, msg):
    msg_list = msg.split(' ')
    len_msg = len(msg_list)
    if msg == 'oripyon':
        return '原始碼請看 https://github.com/leafwind/line_bot'
    elif msg_list[0] == '天氣'.decode('utf-8'):
        return cwb_weather_predictor.predict(msg_list[1].encode('utf-8').replace('台', '臺').decode('utf-8'))
    elif '小路占卜'.decode('utf-8') in msg:
        global maple_phrase
        # profile = line_bot_api.get_profile(uid)
        random.seed(os.urandom(5))
        ph = random.choice(maple_phrase)
        return '今日運勢：{}'.decode('utf-8').format(ph.decode('utf-8'))
    #if '查'.decode('utf-8') in msg:
    #    profile = line_bot_api.get_profile(uid)
    #    print(profile.__dict__)
    #    return '{} 的顯圖：{}, 狀態：{}'.decode('utf-8').format(profile.display_name, profile.picture_url, profile.status_message)
    elif '幫QQ'.decode('utf-8') in msg:
        return '幫QQ喔'
    elif '魔法'.decode('utf-8') in msg:
        return '僕と契約して、魔法少女になってよ！'
    elif 'ㄆㄆ'.decode('utf-8') in msg:
        return 'gmail!'
    elif '請問為什麼'.decode('utf-8') in msg:
        random.seed(os.urandom(5))
        return '因為{}。'.format(random.choice(wtf_reasons.reasons))
    elif '作運動'.decode('utf-8') in msg or '做運動'.decode('utf-8') in msg:
        return 'https://www.facebook.com/dailyheyhey/videos/1721131438179051'
    elif '中文'.decode('utf-8') in msg:
        return '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
    else:
        return None
