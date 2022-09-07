import aio_pika

from queues.core.utils import str_to_datetime
from queues.workers.handlers.handlers import GetHandlers
from queues.schemas.s_general import TaskSchemas, RepeatSchemas
import queues.app_logger as app_logger


logger = app_logger.get_logger(__name__)


async def post_delayed(connection, message: str = None,
                       delay_duration: int = 1, exchange: str = '',
                       routing_key: str = None):
    delay_duration = delay_duration if delay_duration > 0 else 1
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    hold_queue = f"delay.{delay_duration}.{exchange}.{routing_key}"
    hold_queue_arguments = {
        # Exchange where to send messages after TTL expiration.
        "x-dead-letter-exchange": exchange,
        # Routing key which use when resending expired messages.
        "x-dead-letter-routing-key": routing_key,
        # Time in milliseconds
        # after that message will expire and be sent to destination.
        "x-message-ttl": delay_duration,
        # Time after that the queue will be deleted.
        "x-expires": 10000 if delay_duration < 10000 else delay_duration * 2
    }
    # It's necessary to redeclare the queue each time
    #  (to zero its TTL timer).
    routing_key = hold_queue
    queue = await channel.declare_queue(routing_key, durable=True,
                                        exclusive=False,
                                        arguments=hold_queue_arguments)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=message.encode()
        ),
        routing_key=queue.name
    )
    # The channel is expendable.
    await channel.close()


async def check_the_end(task: TaskSchemas) -> bool:
    if task.repeat_schemas == RepeatSchemas.time.value:
        if str_to_datetime() > str_to_datetime(dt=task.expiry):
            logger.info("Completing TIME data processing")
            return True

    if task.repeat_schemas == RepeatSchemas.attempts.value:
        if task.counter == task.attempts:
            logger.info("Completing Data Processing by NUMBER OF TIMES")
            return True

    return False


async def to_handler(task: TaskSchemas) -> bool:
    if not task.handler:
        return False

    handler = GetHandlers(handler_name=task.handler).get_handler()
    handler = handler.value
    handler.set_task(task=task)
    result = await handler.handler()

    return result
