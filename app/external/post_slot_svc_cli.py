import grpc
import underthesea
import json
import sys

from proto.post_slot_service_pb2_grpc import PSServiceStub
from proto.post_slot_service_pb2 import PostSlotRecognizeRequest

# post_formatter
from post_formatter.normalizer import V2PostNormalizer
from post_formatter.elastic_formatter import PostFormatter
normalizer = V2PostNormalizer()
es_formatter = PostFormatter()

class PostSlotServiceClient:
    def __init__(self, config):
        if 'localhost' in config['post_slot_service']['url']:
            channel = grpc.insecure_channel(config['post_slot_service']['url'])
        else:
            credentials = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(config['post_slot_service']['url'], credentials)
        self.__stub = PSServiceStub(channel)
    
    def get_slot_from_posts(self, posts):
        processed_post = []
        for post in posts:
            # Get id of post
            try:
                temp_post = {"id": post["post_id"]}
                # Normalize content before forwarding it through model 
                temp_post['content'] = " ".join(normalizer.v2_normalize(post['content']))
                processed_post.append(temp_post)
                print(str(post) + ' is successful to reformat')
            except Exception as e:
                print(str(post) + ' is failed to reformat because ' + str(e))
            
        # Convert JSON type to string type
        print(processed_post)
        processed_post = json.dumps(processed_post)
        result = self.__stub.PostSlotRecognize(PostSlotRecognizeRequest(message=processed_post))
        # Convert string type to JSON type, After that, Call PostFormatter to format to Elastic Search standard.
        print(json.loads(result.message))
        data_for_es = es_formatter.get_activities(json.loads(result.message))
        
        return data_for_es
