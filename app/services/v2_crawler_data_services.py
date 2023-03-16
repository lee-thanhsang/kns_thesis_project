from facebook_scraper import get_posts
from datetime import datetime

from typing import List, Dict
from app.models import *
import app.models as models 
import app.config as config


class V2CrawlDataService:
    def __init__(self):
        self.__v2_crawler_post = models.V2CrawlerPost()

    def crawl_data_from_facebook(self) -> List[Dict]:
        all_posts: List[Dict] = []
        all_post_to_return = []
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
                    'content': post.get('text'),
                    'post_url': post.get('post_url'),
                    'time': post.get('time')
                }
                posts_list.append(post.get('text'))
                all_posts.append(item)
            
            all_post_to_return.append({page: posts_list})

        if all_posts:
            self.__v2_crawler_post.create_in_batches(all_posts)
        config.lastest_date = datetime.now()
        return all_post_to_return
