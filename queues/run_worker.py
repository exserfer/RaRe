import asyncio
import sys

from queues.schemas.s_general import GeneralQueues
from queues.workers.worker_universal import run_worker


def select_queue(arguments: list = None):
    if not arguments or len(arguments) <= 2:
        return GeneralQueues.router.value

    command = arguments[1]
    queue_name = arguments[2]

    if command not in ["-q", "--queue"]:
        return GeneralQueues.router.value

    if not hasattr(GeneralQueues, queue_name):
        return GeneralQueues.router.value

    return getattr(GeneralQueues, queue_name).value


if __name__ == "__main__":
    if len(sys.argv) > 1:
        queue = select_queue(arguments=sys.argv)
    else:
        queue = 'example'

    print(queue)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_worker(loop, queue_name=queue))
    loop.close()
