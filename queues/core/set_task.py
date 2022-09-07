import aio_pika
import aio_pika.abc

from queues import app_logger
from queues.config import R_CONNECT
from queues.schemas.s_general import GeneralQueues, TaskSchemas


logger = app_logger.get_logger(__name__)


async def set_task(loop, task_param: TaskSchemas,
                   routing_key: str = "router"):

    connection = await aio_pika.connect_robust(R_CONNECT, loop=loop)
    routing_key = getattr(GeneralQueues, routing_key).value
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    queue = await channel.declare_queue(routing_key, durable=True)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=task_param.json().encode()
        ),
        routing_key=queue.name
    )

    logger.info(f" [x] Set Task in queue \"{routing_key}\" => \n{task_param}")

    await connection.close()
