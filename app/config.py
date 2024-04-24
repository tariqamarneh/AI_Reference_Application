from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")

# Database
connection_string = config["DATABASE"]["CONNECTION_STRING"]

# OpenAI
OPENAI_API_KEY = config["AZURE_OPENAI"]["AZURE_OPENAI_API_KEY"]
AZURE_ENDPOINT = config["AZURE_OPENAI"]["AZURE_OPENAI_ENDPOINT"]

# Redis
REDIS_URL = config["REDIS"]["REDIS_URL"]
