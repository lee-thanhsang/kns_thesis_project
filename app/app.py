from flask import Flask
from api import crawler_data_api, chat_bot_api
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, supports_credentials=True)

app.register_blueprint(crawler_data_api.crawler_routes)
app.register_blueprint(chat_bot_api.chatbot_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# from benchmark_tool.querier.querier import *

# benchmark = QueryBenchmark()
# benchmark.run_benchmark(5, keep_activity=True)