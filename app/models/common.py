from pymodm.connection import connect
import certifi

class V2Database:
    def __init__(self):
        self.__database = connect(
            'mongodb+srv://xuannam:xuannamt81@web.qpw3q.mongodb.net/thesis-question', tlsCAFile=certifi.where()
        )