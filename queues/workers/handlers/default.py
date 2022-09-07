from queues.schemas.s_general import TaskSchemas


class Default:
    def __init__(self, task: TaskSchemas = None):
        self.task = task

    @staticmethod
    async def handler():
        return False
