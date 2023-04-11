from flask import Flask
from api import crawler_data_api, chat_bot_api


# app = Flask(__name__, template_folder="templates")

# register_blueprint(crawler_data_api.crawler_routes)
# register_blueprint(chat_bot_api.chatbot_routes)

# run()

from benchmark_tool.querier.querier import *

benchmark = QueryBenchmark()
benchmark.run_benchmark(5, keep_activity=True)