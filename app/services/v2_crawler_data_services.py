from facebook_scraper import get_posts
from datetime import datetime

from typing import List, Dict
from models import *
import models as models 
import config as config

class V2CrawlDataService:
    def __init__(self, config, post_slot_svc_cli, es_client):
        self.__post_slot_svc_cli = post_slot_svc_cli
        self.__es_client = es_client
        self.__crawler_config = config['crawler']
        self.__v2_crawler_post = models.v2_crawl_data_model.V2CrawlerPost()

    def crawl_data_from_facebook(self) -> List[Dict]:
        v2_crawler_post = self.__v2_crawler_post
        lastest_time = v2_crawler_post.get_time_point()
        print('LATEST TIME ', lastest_time)
        # Convert to datetime
        lastest_time = datetime.strptime(lastest_time, "%Y-%m-%d %H:%M:%S")

        all_posts: List[Dict] = []

        fanpages = self.__crawler_config['fanpage_links'].split(',')
        for page in fanpages:

            posts_from_page = get_posts(
                page,
                options={
                    "comments": False,
                    "reactions": False,
                    "allow_extra_requests": True,
                    "posts_per_page": 2000,
                },
                timeout=120,
                pages=10,
                cookies=self.__crawler_config['cookie_path'],
                extra_info=True,
                latest_date=lastest_time
            )

            for post in posts_from_page:
                item = {
                    'post_id': post.get('post_id'),
                    'content': post.get('text') or post.get('post_text'),
                    'post_url': post.get('post_url'),
                    'time': post.get('time')
                }

                print(str(item) + 'has been added')
                if item.get('content'):
                    all_posts.append(item)
                
        print('Done Crawl')
        if all_posts:
            v2_crawler_post.create_in_batches(all_posts)
            self.import_data_to_elastic_search(all_posts)
        
        v2_crawler_post.update_time_point()

    def import_data_to_elastic_search(self, posts):
        posts_for_es = self.__post_slot_svc_cli.get_slot_from_posts(posts)
        es_client = self.__es_client
        
        for post_for_es in posts_for_es:
            try:
                post_for_es['activity']['timestamp'] = datetime.now()
                if 'name' not in post_for_es['activity']:
                    continue

                if 'meetgooglecom' in post_for_es['activity']['name']:
                    continue

                es_client.insert_one('thesis', post_for_es['post_id'], post_for_es['activity'])
                print(str(post_for_es) + 'is inserted to elasticsearch')
            except Exception as e:
                print(e)
