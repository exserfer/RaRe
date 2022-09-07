from typing import Any

from queues.schemas.s_general import TaskSchemas


class IntegrationsHandlers:
    def __init__(self, handler: Any = None,
                 handler_name: str = None,
                 task: TaskSchemas = None):
        self._handler = handler
        self.handler_name = handler_name
        self.task = task

    async def get_sub_handler(self):
        return NotImplemented

    async def handler(self):
        return NotImplemented

    def set_task(self, task: TaskSchemas):
        self.task = task
