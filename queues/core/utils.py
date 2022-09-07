from datetime import datetime

from queues.schemas.s_general import GeneralQueues, TaskSchemas


def str_to_datetime(dt: str = None):
    if dt is None:
        dt = str(datetime.now()).split(".")[0]

    get_datetime = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    return get_datetime


def update_task(task: TaskSchemas = None,
                target_queue: str = None) -> None | TaskSchemas:
    if not task or not target_queue:
        return None

    queues_road = task.queue_sequence.get('queues_road', None)

    if not queues_road or len(queues_road) == 0:
        return None

    new_task = TaskSchemas(**task.dict())
    handler_next_queue = task.queue_sequence.get(target_queue, None)
    if not handler_next_queue:
        return None

    new_handler = handler_next_queue.get('handler', None)
    new_sub_handler = handler_next_queue.get('sub_handler', None)

    if new_handler is None or new_sub_handler is None:
        return None

    new_task.handler = new_handler
    new_task.sub_handler = new_sub_handler
    new_task.counter = 0
    new_task.target_queue = target_queue
    new_task.uuid_task = task.uuid_task

    return new_task


def check_exist_queues(all_queues: GeneralQueues, q_name: str = None) -> bool:
    if not q_name:
        return False

    is_exist = False
    for q_item in all_queues:
        is_exist = True if str(q_item.value) == q_name else False
        if is_exist:
            return True

    return is_exist


def next_queue(queue_sequence: dict = None,
               current_queue: str = None) -> str | None:
    if queue_sequence is None or current_queue is None:
        return None

    queues_road = queue_sequence.get('queues_road', False)

    if not queues_road or len(queues_road) == 0:
        return None

    if current_queue not in queues_road:
        return None

    index = [i for i, x in enumerate(queues_road) if current_queue in x][0]
    next_queue = None if len(queues_road) == index+1 else queues_road[index+1]

    if next_queue is None:
        return None

    return next_queue if check_exist_queues(all_queues=GeneralQueues,
                                            q_name=next_queue) else None
