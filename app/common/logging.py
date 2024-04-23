import logging
import datetime


class MongoHandler(logging.Handler):

    def __init__(
        self, connection=None, database="AI_Reference_Application", collection="logs"
    ):
        super().__init__()
        self.connection = connection
        self.database = self.connection[database]
        self.collection = self.database[collection]
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        self.collection.insert_one(
            {
                "when": datetime.datetime.now(),
                "filename": record.filename,
                "funcName": record.funcName,
                "levelname": record.levelname,
                "message": record.msg,
            }
        )
