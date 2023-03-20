from flask import Flask
from app.api import routes

app = Flask(__name__, template_folder="templates")

app.register_blueprint(routes)
