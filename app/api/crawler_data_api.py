from flask import Blueprint
from flask import Flask, request, render_template, redirect
import services as services

crawler_routes = Blueprint("crawler_routes", __name__)

@crawler_routes.route('/v2/crawl-data-from-facebook', methods=['GET'])
def crawl_data_from_facebook_handler():
    posts = services.v2_crawler_data_services.V2CrawlDataService().crawl_data_from_facebook()
    return posts
