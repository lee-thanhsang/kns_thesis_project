from flask import Blueprint
from flask import Flask, request, render_template, redirect, make_response
from server.server import *
from utils.cookie.cookie_generator import *
import threading
import traceback
import requests
import os
import time

chatbot_routes = Blueprint("chatbot_routes", __name__)

COOKIE_KEY = 'kns_chat_bot_user_id'
VERIFY_TOKEN = 'kns-chatbot'
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN') or 'EAABebNlZAZBysBAFk0ZC2KKcQhBZALHSh0cSnQ9yAugNGrHZBP8gmpU8xrh1DCU0WymZBWNWJ3Umxbn4dfeSbcpT6jMDiENZCrQ8wtdMYW34PXlcRv2uPzQiXoJTdZARBlt1er0K6lQYEvDVIDUxLX4kwg9Gv8OlLUGHybmehN6NskK7rjiqzyDXqAnXgZCpAzJ8ZD'
OFFICIAL_ACCESS_TOKEN = os.getenv('OFFICIAL_ACCESS_TOKEN') or 'EAADQaUxEoXkBANz01TrbL2Sek4YMHa42komGh3f0SOuwRaCszWa6gRh03XSzOKaWRRD8r3oDDO0614uYBewn75XUxPT37RblRPx2DmIRcwM9uGp2pHZB2TlLw1ZAA3ZCF9FtOVLWL3ZBEPhziIu9fkMFQvWqVJ5TN9VjN6HqZC09vWBZChLNqx'

@chatbot_routes.route('/', methods=['GET', 'POST'])
def get_chat_bot_interface():
    return render_template('index.html')

@chatbot_routes.route('/v2/get-response-sentence', methods=['POST'])
def get_intent_from_message():
    data = request.form.to_dict()
    user_id = request.cookies.get(COOKIE_KEY)
    log = {}
    try:
        message_id = str(time.time())
        response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(data['sentence'], message_id, user_id, ACCESS_TOKEN, log)
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
        # server.redis.remove_by_key('messages:' + user_id)

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
            message_id = message['message'].get('mid')
            print('sentence ', sentence)
            if user_id and sentence and message_id:
                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_on'
                }
                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
                
                prev_message = server.redis.get_value_from_key('users:' + user_id + ':messages:' + message_id)
                if prev_message:
                    print('retry webhook detection')
                    return 'ok'
                
                log = {}
                try:
                    response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(sentence, message_id, user_id, log, ACCESS_TOKEN, True)
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
                
                if len(output_sentence) > 0:
                    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
                    print('content ', resp.content)

                # Store to clickhouse.
                thread = threading.Thread(target=server.clickhouse_client.create_dialog, kwargs={'log': log})
                thread.start()

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_off'
                }
                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

                # server.redis.remove_by_key('messages:' + user_id)

                return 'ok'

        # Create response and cookies
        # resp = make_response({'sentence': output_sentence})
        # if user_id:
        #     resp.set_cookie(COOKIE_KEY, user_id)


        return 'ok'
    
    return 'Unavailabel method'


@chatbot_routes.route('/webhooks/facebook/webhook', methods=['POST', 'GET'])
def get_intent_from_message_from_webhook_official():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        
        return 'Verified token is invalid'

    elif request.method == 'POST':
        output = request.get_json()
        print(output)
        event = output['entry'][0]
        messaging = event.get('messaging') or event.get('sender')
        if not messaging or len(messaging) == 0:
            return 'ok'
        
        message = messaging[0]
        
        if message.get('message'):
            user_id = message['sender']['id']
            print('user id ', user_id)
            sentence = message['message'].get('text')
            message_id = message['message'].get('mid')
            print('sentence ', sentence)
            if user_id and sentence and message_id:
                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_on'
                }
                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                print('content ', resp.content)

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_on'
                }
                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                
                prev_message = server.redis.get_value_from_key('users:' + user_id + ':messages:' + message_id)
                if prev_message:
                    print('retry webhook detection')
                    return 'ok'
                
                log = {}
                quick_replies = None
                try:
                    response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(sentence, message_id, user_id, log, OFFICIAL_ACCESS_TOKEN, True)
                    output_sentence = server.v2_response_sentence.make_response_sentence(response_sentence)
                    if isinstance(output_sentence, list):
                        quick_replies = output_sentence[1]
                        output_sentence = output_sentence[0]

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

                if quick_replies:
                    data['message']['quick_replies'] = []
                    for reply in quick_replies:
                        quick_reply = {
                            'content_type': 'text',
                            'title': reply,
                            'payload': reply,
                        }

                        data['message']['quick_replies'].append(quick_reply)
                
                if len(output_sentence) > 0:
                    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                    print('content ', resp.content)

                # Store to clickhouse.
                thread = threading.Thread(target=server.clickhouse_client.create_dialog, kwargs={'log': log})
                thread.start()

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_off'
                }
                resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)

                # server.redis.remove_by_key('messages:' + user_id)

                return 'ok'

        # Create response and cookies
        # resp = make_response({'sentence': output_sentence})
        # if user_id:
        #     resp.set_cookie(COOKIE_KEY, user_id)


        return 'ok'
    
    return 'Unavailabel method'

@chatbot_routes.route('/webhooks/facebook/webhook/test', methods=['POST', 'GET'])
def get_intent_from_message_from_webhook_test():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        
        return 'Verified token is invalid'

    elif request.method == 'POST':
        output = request.get_json()
        print(output)
        event = output['entry'][0]
        messaging = event.get('messaging') or event.get('sender')
        if not messaging or len(messaging) == 0:
            return 'ok'
        
        message = messaging[0]
        
        if message.get('message'):
            user_id = message['sender']['id']
            print('user id ', user_id)
            sentence = message['message'].get('text')
            message_id = message['message'].get('mid')
            print('sentence ', sentence)
            if user_id and sentence and message_id:
                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_on'
                }
                # resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                # print('content ', resp.content)

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_on'
                }
                # resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                
                prev_message = server.redis.get_value_from_key('users:' + user_id + ':messages:' + message_id)
                if prev_message:
                    print('retry webhook detection')
                    return 'ok'
                
                log = {}
                quick_replies = None
                try:
                    response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(sentence, message_id, user_id, log, OFFICIAL_ACCESS_TOKEN, False)
                    output_sentence = server.v2_response_sentence.make_response_sentence(response_sentence)
                    if isinstance(output_sentence, list):
                        quick_replies = output_sentence[1]
                        output_sentence = output_sentence[0]

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

                if quick_replies:
                    data['message']['quick_replies'] = []
                    for reply in quick_replies:
                        quick_reply = {
                            'content_type': 'text',
                            'title': reply,
                            'payload': reply,
                        }

                        data['message']['quick_replies'].append(quick_reply)
                
                # if len(output_sentence) > 0:
                #     resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)
                #     print('content ', resp.content)

                # Store to clickhouse.
                # thread = threading.Thread(target=server.clickhouse_client.create_dialog, kwargs={'log': log})
                # thread.start()

                data = {
                    'recipient': {
                        'id': user_id
                    },
                    'sender_action': 'typing_off'
                }
                # resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + OFFICIAL_ACCESS_TOKEN, json=data)

                # server.redis.remove_by_key('messages:' + user_id)

                return output_sentence

        # Create response and cookies
        # resp = make_response({'sentence': output_sentence})
        # if user_id:
        #     resp.set_cookie(COOKIE_KEY, user_id)


        return 'ok'
    
    return 'Unavailabel method'
