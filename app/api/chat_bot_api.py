from flask import Blueprint
from flask import Flask, request, render_template, redirect, make_response
from server.server import *
from utils.cookie.cookie_generator import *
import threading

chatbot_routes = Blueprint("chatbot_routes", __name__)

COOKIE_KEY = 'kns_chat_bot_user_id'

@chatbot_routes.route('/', methods=['GET'])
def get_chat_bot_interface():
    return render_template('index.html')

@chatbot_routes.route('/v2/get-response-sentence', methods=['POST'])
def get_intent_from_message():
    try:
        data = request.form.to_dict()
        user_id = request.cookies.get(COOKIE_KEY)
        log = {}
        response_sentence, user_id = server.v2_response_sentence.get_intent_and_slot_from_sentence(data['sentence'], user_id, log)
        output_sentence = server.v2_response_sentence.make_response_sentence(response_sentence)
        log['raw_response'] = str(output_sentence)
        
    except Exception as e:
        output_sentence = 'Hệ thống gặp lỗi khi xử lý tin nhắn của bạn. Xin lỗi vì sự bất tiện này.'
        log['raw_response'] = str(e)

    # Create response and cookies
    resp = make_response({'sentence': output_sentence})
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