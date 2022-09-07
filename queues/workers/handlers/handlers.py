from enum import Enum

from queues.workers.handlers.default import Default
from queues.workers.handlers.example import Example


class Handlers(Enum):
    default = Default()
    example = Example()


class GetHandlers:
    def __init__(self, handler_name: str = None):
        self.handler_name = handler_name

    def get_handler(self):
        return getattr(Handlers, self.handler_name)
