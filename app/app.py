from flask import Flask
from app.api import *

app = Flask(__name__, template_folder="templates")

app.register_blueprint(crawler_data_api.crawler_routes)
app.register_blueprint(chat_bot_api.chatbot_routes)

