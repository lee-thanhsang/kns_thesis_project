from pymodm import MongoModel, fields

class V2RawPostModel(MongoModel):
    _id = fields.ObjectIdField(primary_key=True)
    content = fields.CharField()
    post_url = fields.CharField()
    time = fields.CharField()
