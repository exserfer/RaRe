import os

import pymongo
from dotenv import dotenv_values, load_dotenv


DEBUG = True

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config = {
    **dotenv_values(".env"),
    **os.environ,
}

# RabbitMQ
R_PROTOCOL = config.get("R_PROTOCOL", False)
R_HOST = config.get("R_HOST", False)
R_PORT = config.get("R_PORT", False)
R_USER = config.get("R_USER", False)
R_PWD = config.get("R_PWD", False)
R_CONNECT = f"{R_PROTOCOL}://{R_USER}:{R_PWD}@{R_HOST}:{R_PORT}/"

# Establish connection to MongoDB
# MongoDB must be running on the computer, 27017 is the standard port
MONGO_USER = config.get("MNG_USER", False)
MONGO_PWD = config.get("MNG_PWD", False)
MONGO_HOST = config.get("MNG_HOST", False)
MONGO_PORT = config.get("MNG_PORT", False)
mongo_connect = pymongo.MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}/")
# Collections settings to work with mongo
MONGO_DB__HORO = config.get("MNG_DB", False)

TIMEZONE_DEFAULT = config.get("TIMEZONE_DEFAULT", False)
