import asyncio
import copy
from enum import Enum

import httpx
from bson import ObjectId
from pydantic import ValidationError

from queues import app_logger
from queues.core.crud_mongo import ToMongo
from queues.workers.handlers.sub_handlers.s_example import ExampleData

logger = app_logger.get_logger(__name__)


class ExampleSubHandlers(str, Enum):
    example = "example"
    example_second = "example_second"


class ExampleAPIURLs(str, Enum):
    base_url = "https://jsonplaceholder.typicode.com"
    posts = "/posts"  # base_url + "/posts/{id:int}"


async def get_fake_posts(post_id: int = 0):
    url = str(ExampleAPIURLs.base_url.value) + str(ExampleAPIURLs.posts.value)
    url = url + f"/{post_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        try:
            example_data = ExampleData(**r.json())
        except ValidationError as e:
            logger.info(e)
            return False

        # Create Mongo-Object
        item = ToMongo(target_coll="example")
        _id = await put_in_mongo_db(item=item, data=example_data.dict())

        if isinstance(_id, bool) and _id is False:
            return False

    return True


async def put_in_mongo_db(item: ToMongo, data: dict):
    # Check exist object bellow will put in the database
    rm_list = ["body"]
    filter_set = copy.deepcopy(data)
    [filter_set.pop(key) for key in rm_list]

    _id: ObjectId | bool = await item.set_data_before_exist(
        payload=data,
        filter_set=filter_set)

    return _id


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_fake_posts(post_id=6))
    loop.close()
