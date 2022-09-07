import asyncio
import json

import aio_pika
import aio_pika.abc

from pydantic import ValidationError

from queues import app_logger
from queues.config import R_CONNECT
from queues.core.set_task import set_task
from queues.core.to_repeats import ToRepeat
from queues.core.utils import next_queue, update_task

from queues.schemas.s_general import GeneralQueues, TaskSchemas
from queues.workers.worker_utils import post_delayed, to_handler, check_the_end


logger = app_logger.get_logger(__name__)


def select_queue(arguments: list = None):
    if not arguments or len(arguments) <= 2:
        return GeneralQueues.default.value

    command = arguments[1]
    queue_name = arguments[2]

    if command not in ["-q", "--queue"]:
        return GeneralQueues.default.value

    if not hasattr(GeneralQueues, queue_name):
        return GeneralQueues.default.value

    return getattr(GeneralQueues, queue_name).value


async def run_worker(loop, queue_name: str = str(GeneralQueues.fallen.value)):
    connection = await aio_pika.connect_robust(R_CONNECT, loop=loop)

    async with connection:
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            durable=True
        )

        print("[X] Waiting New task... For STOP, press CTRL+C")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    msg = message.body.decode()

                    try:
                        task = TaskSchemas(**json.loads(msg))
                    except ValidationError:
                        logger.warning(f"ValidationError: {msg}")
                        await post_delayed(
                            connection,
                            message=msg,
                            delay_duration=1,
                            exchange='',
                            routing_key=str(GeneralQueues.fallen.value))

                    task.counter = task.counter + 1
                    check_end: bool = await check_the_end(task=task)

                    if check_end:
                        logger.info(f"update_task: {task.dict()}")
                        await post_delayed(
                            connection,
                            message=task.json(),
                            delay_duration=1,
                            exchange='',
                            routing_key=str(GeneralQueues.fallen.value))
                    else:
                        try:
                            # Sending for processing.
                            # First the handler is selected, then the handler
                            # itself is selected
                            # sub_handler is the final handler
                            # In case of an error we return False
                            result: bool = await to_handler(task=task)

                            if result is False:
                                raise Exception

                            # If the task is done, we check if it needs
                            # to be sent to the next queue.
                            # And if it does, we send it
                            q_for_next_step: str | None = next_queue(
                                queue_sequence=task.queue_sequence,
                                current_queue=queue_name)
                            if q_for_next_step:
                                # First you must modify or create parameters
                                # for the queue
                                new_task = update_task(
                                    task=task,
                                    target_queue=q_for_next_step)
                                # Then send it to the next queue
                                await set_task(loop,
                                               task_param=new_task,
                                               routing_key=q_for_next_step)

                        except Exception as e:
                            logger.exception(e)
                            time_delay: int = ToRepeat(
                                type_delay=task.type_repeat,
                                evenly_delay=100,
                                counter=task.counter).get_delay()
                            await post_delayed(connection, message=task.json(),
                                               delay_duration=time_delay,
                                               exchange='',
                                               routing_key=queue_name)

                    print("[X] Waiting other message. For STOP, press CTRL+C")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        run_worker(loop, queue_name=str(GeneralQueues.default.value)))
    loop.close()
