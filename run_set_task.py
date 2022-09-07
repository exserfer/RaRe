import asyncio
from random import randint
import uuid

from queues.core.set_task import set_task
from queues.schemas.s_general import GeneralQueues, TaskSchemas, TypeRepeat
from queues.workers.handlers.sub_handlers.example import ExampleSubHandlers


if __name__ == "__main__":
    queue_sequence = {
        "queues_road": [GeneralQueues.example.value],
        GeneralQueues.example.value: {
            "handler": GeneralQueues.example.value,
            "sub_handler": ExampleSubHandlers.example.value}
    }

    task_param = TaskSchemas(
        target_queue=GeneralQueues.example.value,
        type_repeat=TypeRepeat.fibo.value,
        queue_sequence=queue_sequence,
        uuid_task=uuid.uuid4().hex,
        handler=GeneralQueues.example.value,
        sub_handler=str(ExampleSubHandlers.example.value),
        payload=randint(0, 100)
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(set_task(
        loop, task_param=task_param,
        routing_key=str(GeneralQueues.example.value)))
    loop.close()
