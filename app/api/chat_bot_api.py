from flask import Blueprint
from flask import Flask, request, render_template, redirect
import app.services as services

chatbot_routes = Blueprint("chatbot_routes", __name__)

@chatbot_routes.route('/', methods=['GET'])
def get_chat_bot_interface():
    return render_template('chat.html')

@chatbot_routes.route('/v2/get-responce-sentence', methods=['POST'])
def get_intent_from_message():
    data = request.form.to_dict()
    responce_sentence = services.v2_response_senetence.V2ResponseSentenceService().get_intent_and_slot_from_sentence(data['sentence'])
    return {'sentence': str(responce_sentence)}
