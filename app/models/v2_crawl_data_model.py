from datetime import datetime

from pymodm import MongoModel, fields
from typing import List, Dict
from models.common import V2Database


class V2RawPostModel(MongoModel):
    _id = fields.ObjectIdField(primary_key=True)
    content = fields.CharField()
    post_url = fields.CharField()
    time = fields.CharField()


class V2TimePointCrawlData(MongoModel):
    _id = fields.ObjectIdField(primary_key=True)
    key = fields.CharField()
    time_point = fields.CharField()

class V2CrawlerPost(V2Database):
    def __init__(self):
        super().__init__()

    def create_in_batches(self, posts: List[Dict]):
        post_lists_normalized: List[V2RawPostModel] = []
        for post in posts:
            item = V2RawPostModel(
                content=post.get('content'),
                post_url=post.get('post_url'),
                time=post.get('time')
            )

            post_lists_normalized.append(item)

        V2RawPostModel.objects.bulk_create(post_lists_normalized)

    def get_time_point(self):
        timepoint_model = V2TimePointCrawlData.objects
        check_point = list(timepoint_model.raw({'key': 'kns_time_point'}))

        if check_point:
            return check_point[0].time_point
        else:
            timepoint_model.bulk_create([V2TimePointCrawlData(key='kns_time_point', time_point='2023-05-01 00:00:00')])
            return '2023-05-01 00:00:00'
        
    def update_time_point(self):
        now_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'

        V2TimePointCrawlData.objects.raw({'key': 'kns_time_point'}).update(
            {"$set": {"time_point": now_string}},
            upsert=True
        )
