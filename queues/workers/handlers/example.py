from enum import Enum

from queues import app_logger

from queues.workers.handlers.integrations_handler import IntegrationsHandlers
from queues.workers.handlers.sub_handlers.example import get_fake_posts


logger = app_logger.get_logger(__name__)


class Example(IntegrationsHandlers):

    async def get_sub_handler(self):
        class SubHandler(Enum):
            example = self.example
            example_second = self.example_second

        sub_handler = self.task.sub_handler
        current_handler = hasattr(SubHandler, sub_handler)

        if current_handler:
            result = getattr(SubHandler, sub_handler)
            return await result.__call__()

        return False

    async def handler(self) -> bool:
        logger.info("EXAMPLE_HANDLER")
        return await self.get_sub_handler()

    async def example(self) -> bool:
        try:
            payload = self.task.payload
            content = await get_fake_posts(post_id=payload)
            logger.info(content)
        except Exception as e:
            logger.info(e)
            return False

        return True

    async def example_second(self) -> bool:
        try:
            payload = self.task.payload
            content = await get_fake_posts(post_id=payload)
            logger.info(content)
        except Exception as e:
            logger.info(e)
            return False

        return True
