from flask import Blueprint
from flask import Flask, request, render_template, redirect, make_response
from server import *
from utils.cookie.cookie_generator import *
import time

chatbot_routes = Blueprint("chatbot_routes", __name__)

COOKIE_KEY = 'kns_chat_bot_user_id'

@chatbot_routes.route('/', methods=['GET'])
def get_chat_bot_interface():
    return render_template('index.html')

@chatbot_routes.route('/v2/get-response-sentence', methods=['POST'])
def get_intent_from_message():
    data = request.form.to_dict()
    user_id = request.cookies.get(COOKIE_KEY)
    log = {}
    response_sentence, user_id = server.server.v2_response_sentence.get_intent_and_slot_from_sentence(data['sentence'], user_id, log)
    output_sentence = server.server.v2_response_sentence.make_response_sentence(response_sentence)
    log['raw_response'] = str(output_sentence)
    resp = make_response({'sentence': output_sentence})
    resp.set_cookie(COOKIE_KEY, user_id)

    return resp
