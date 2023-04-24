from flask import Blueprint
from flask import Flask, request, render_template, redirect, make_response
from server.server import *
from utils.cookie.cookie_generator import *
import threading
import traceback
import requests
import os

chatbot_routes = Blueprint("chatbot_routes", __name__)

COOKIE_KEY = 'kns_chat_bot_user_id'
VERIFY_TOKEN = 'kns-chatbot'
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN') or 'EAABebNlZAZBysBACXEFTjmv1sxQWVhDRKZA5VVtwEl19VXpFGU8tfZClrazKRY3ixZBD02D52dTo9azCIDlqKDeCRa70x67nh57LOR29vEmT27WkHWYfv60ZAjYnCqsh84hxdxo3zfRXJgIZB4lHZAzzyRZBhG8wksbqi5tW87rYTu1ATpZCJ067OAZCUMMnLUArbcZD'


@chatbot_routes.route('/', methods=['GET'])
def get_chat_bot_interface():
    return render_template('index.html')

@chatbot_routes.route('/v2/get-response-sentence', methods=['POST'])
def get_intent_from_message():
    data = request.form.to_dict()
    user_id = request.cookies.get(COOKIE_KEY)
    log = {}
    try:
        response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(data['sentence'], user_id, log)
        output_sentence = server.v2_response_sentence.make_response_sentence(response_sentence)
        log['raw_response'] = str(output_sentence)
        
    except Exception as e:
        output_sentence = 'Hệ thống gặp lỗi khi xử lý tin nhắn của bạn. Xin lỗi vì sự bất tiện này.'
        log['raw_response'] = str(traceback.format_exc())
        traceback.print_exc()

    # Create response and cookies
    resp = make_response({'sentence': output_sentence})
    if user_id:
        resp.set_cookie(COOKIE_KEY, user_id)

    # Store to clickhouse.
    thread = threading.Thread(target=server.clickhouse_client.create_dialog, kwargs={'log': log})
    thread.start()

    return resp

@chatbot_routes.route('/v2/end-dialog', methods=['POST', 'GET'])
def end_dialog():
    data = request.form.to_dict()
    user_id = request.cookies.get(COOKIE_KEY)
    if user_id:
        server.v2_response_sentence.end_dialog(user_id)
    
    resp = make_response({'sentence': 'complete'})
    resp.set_cookie(COOKIE_KEY, user_id)

    return resp

@chatbot_routes.route('/v2/webhooks/facebook/webhook', methods=['POST', 'GET'])
def get_intent_from_message_from_webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        
        return 'Verified token is invalid'

    elif request.method == 'POST':
        output = request.get_json()
        event = output['entry'][0]
        messaging = event['messaging']
        message = messaging[0]
        
        if message.get('message'):
            user_id = message['sender']['id']
            print('user id ', user_id)
            sentence = message['message'].get('text')
            print('sentence ', sentence)
            if user_id and sentence:
                prev_message = server.redis.get_value_from_key('messages:' + user_id)
                if prev_message and prev_message.decode('utf-8') == sentence:
                    print('retry webhook detection')
                    return 'ok'


                log = {}
                try:
                    response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(sentence, user_id, log)
                    output_sentence = server.v2_response_sentence.make_response_sentence(response_sentence)
                    log['raw_response'] = str(output_sentence)
                    
                except Exception as e:
                    output_sentence = 'Chúng mình gặp lỗi khi xử lý tin nhắn của bạn. Xin lỗi vì sự bất tiện này.'
                    log['raw_response'] = str(traceback.format_exc())
                    traceback.print_exc()

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'message': {
                        'text': output_sentence
                    }
                }

                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
                print('content ', resp.content)

                # Store to clickhouse.
                thread = threading.Thread(target=server.clickhouse_client.create_dialog, kwargs={'log': log})
                thread.start()

                return 'ok'

        # Create response and cookies
        # resp = make_response({'sentence': output_sentence})
        # if user_id:
        #     resp.set_cookie(COOKIE_KEY, user_id)


        return 'ok'
    
    return 'Unavailabel method'
