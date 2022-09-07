import asyncio
import sys

from queues.workers.worker_universal import run_worker, select_queue


if __name__ == "__main__":
    if len(sys.argv) > 1:
        queue = select_queue(arguments=sys.argv)
    else:
        queue = 'example'

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_worker(loop, queue_name=queue))
    loop.close()
