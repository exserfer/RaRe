from types import NoneType
from bson.objectid import ObjectId

from queues import app_logger
from queues.config import mongo_connect, MONGO_DB__HORO


logger = app_logger.get_logger(__name__)


class ToMongo:
    """
    With this class we put and read data from the MongoBase
    set_horo = HoroNoSQLDB(mongo_connect=mongo_connect,
                           current_db=current_db,
                           target_coll=target_coll)
    await set_horo.set_data_in_collections(payload=payload)
    """

    # connect to database, if it does not exist, it will be created
    # dictionary style

    def __init__(self, connect: str = mongo_connect,
                 # Name of the database where we're looking for the information
                 current_db: str = MONGO_DB__HORO,
                 # The current collection we're working with
                 target_coll: str = 'default'):
        self.mongo_connect = connect
        self.current_db = current_db
        self.target_coll = target_coll

    # Put it in the database, in the selected collection with
    # the necessary scheme
    async def set_data(self, payload: str | dict = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        ins_result = collection.insert_one(payload)
        id_items = ins_result.inserted_id

        return id_items

    async def set_data_before_exist(self,
                                    payload: str | dict = None,
                                    filter_set: dict = None) -> ObjectId | bool:
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]

        exist_item = collection.find_one(filter_set)
        if type(exist_item) is NoneType:
            try:
                ins_result = collection.insert_one(payload)
                return ins_result.inserted_id
            except Exception as e:
                logger.info(e)
                return False

        return exist_item.get("_id", False)

    # Search the database for the keys we received
    async def get_data(self, payload: dict = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        item_result = collection.find_one(payload)

        if type(item_result) is NoneType:
            return False

        id_items = item_result.get('_id', False)

        return id_items

    async def get_data_all(self, payload: dict = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        items_result = collection.find(payload)

        if type(items_result) is NoneType:
            return False

        return items_result

    async def get_item_by_id(self, _id: str = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        try:
            item_result = collection.find_one({"_id": ObjectId(_id)})
        except Exception as e:
            logger.info(e)
            return None

        if type(item_result) is NoneType:
            return None

        return item_result

    # Search the database for the received keys and RETURN ALL POLES
    async def get_all_data(self, payload: dict = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        item_result = collection.find_one(payload)

        if type(item_result) is NoneType:
            return False

        return item_result

    async def update_item(self, filter_: dict = None,
                          payload: str | dict = None):
        current_db = mongo_connect[self.current_db]
        collection = current_db[self.target_coll]
        collection.update_one(filter_, {'$set': payload})
        item_result = collection.find_one(filter_)

        return item_result
