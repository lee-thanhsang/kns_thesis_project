from flask import Blueprint
import app.services as services

routes = Blueprint("routes", __name__)

@routes.route('/', methods=['GET'])
def hello():
    return "Hello KNS"

@routes.route('/v2/crawl-data-from-facebook', methods=['GET'])
def crawl_data_from_facebook_handler():
    posts = services.V2CrawlDataService.crawl_data_from_facebook()
    return posts
