from pymodm import MongoModel, fields
from typing import List, Dict
from models.common import V2Database


class V2RawPostModel(MongoModel):
    _id = fields.ObjectIdField(primary_key=True)
    content = fields.CharField()
    post_url = fields.CharField()
    time = fields.CharField()


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