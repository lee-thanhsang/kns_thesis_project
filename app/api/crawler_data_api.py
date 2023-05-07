from flask import Blueprint
from flask import Flask, request, render_template, redirect
import services as services
from server.server import *

crawler_routes = Blueprint("crawler_routes", __name__)

@crawler_routes.route('/v2/crawl-data-from-facebook', methods=['GET'])
def crawl_data_from_facebook_handler():
    server.v2_process_post_slot.crawl_data_from_facebook()
    return 'Successful'
