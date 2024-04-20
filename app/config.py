from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")

# Database
connection_string = config["DATABASE"]["CONNECTION_STRING"]

# API
OPENAI_API_KEY = config["AZURE_OPENAI"]["AZURE_OPENAI_API_KEY"]
AZURE_ENDPOINT = config["AZURE_OPENAI"]["AZURE_OPENAI_ENDPOINT"]
