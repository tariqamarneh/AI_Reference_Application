import logging as log

from app.common.logging import MongoHandler
from app.common.database import get_connection


connection = get_connection()
mongo_logger = log.getLogger("AI_Reference_Application_mongo_Logs")
mongo_logger.setLevel(log.DEBUG)
mongo_logger.addHandler(
    MongoHandler(database="AI_Reference_Application", connection=connection)
)
