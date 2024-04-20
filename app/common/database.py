import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import connection_string


def get_connection():
    connection = AsyncIOMotorClient(connection_string)
    return connection
