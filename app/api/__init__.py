from flask import Blueprint
from flask import Flask, request, render_template, redirect
import app.services as services

routes = Blueprint("routes", __name__)

@routes.route('/', methods=['GET'])
def hello():
    return "Hello KNS"

@routes.route('/v2/crawl-data-from-facebook', methods=['GET'])
def crawl_data_from_facebook_handler():
    posts = services.v2_crawler_data_services.V2CrawlDataService().crawl_data_from_facebook()
    return posts

@routes.route('/v2/get-responce-sentence', methods=['POST'])
def get_intent_from_message():
    data = request.form.to_dict()
    responce_sentence = services.v2_response_senetence.V2ResponseSentenceService().output_responce_sentence(data['sentence'])
    return {'sentence': responce_sentence}

@routes.route('/v2/chat-bot', methods=['GET'])
def get_chat_bot_interface():
    return render_template('chat.html')
