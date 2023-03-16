from typing import List, Dict
from pymodm.connection import connect
from app.models.v2_raw_post_model import V2RawPostModel
import certifi

class V2Database:
    def __init__(self):
        self.__database = connect(
            'mongodb+srv://xuannam:xuannamt81@web.qpw3q.mongodb.net/thesis-question', tlsCAFile=certifi.where()
        )

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