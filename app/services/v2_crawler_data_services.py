from facebook_scraper import get_posts
from datetime import datetime
import json

from typing import List, Dict
from models import *
import models as models 
import config as config

class V2CrawlDataService:
    def __init__(self, post_slot_svc_cli, es_client):
        self.__post_slot_svc_cli = post_slot_svc_cli
        self.__es_client = es_client
        self.__v2_crawler_post = models.v2_crawl_data_model.V2CrawlerPost()

    def crawl_data_from_facebook(self) -> List[Dict]:
        all_posts: List[Dict] = []

        for page in config.FANPAGE_LINKS:
            posts_list = []
            posts_from_page = get_posts(
                page,
                options={
                    "comments": False,
                    "reactions": False,
                    "allow_extra_requests": True,
                    "posts_per_page": 200,
                },
                extra_info=True,
                pages=100,
                cookies=config.COOKIE_PATH,
                latest_date=config.lastest_date
            )

            for post in posts_from_page:
                item = {
                    'post_id': post.get('post_id'),
                    'content': post.get('text'),
                    'post_url': post.get('post_url'),
                    'post_time': post.get('time')
                }
                posts_list.append(post.get('text'))
                all_posts.append(item)

        if all_posts:
            self.__v2_crawler_post.create_in_batches(all_posts)
        
        config.lastest_date = datetime.now()

        self.import_data_to_elastic_search(all_posts)

    def import_data_to_elastic_search(self, posts):
        posts_for_es = self.__post_slot_svc_cli.get_slot_from_posts(posts)

        es_client = self.__es_client
        
        for post_for_es in posts_for_es:
            try:
                es_client.insert_one('thesis', post_for_es['post_id'], post_for_es['activity'])
            except:
                pass
