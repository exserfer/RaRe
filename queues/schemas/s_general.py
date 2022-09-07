from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel


class GeneralQueues(str, Enum):
    router = "router"
    example = "example"
    default = "default"
    fallen = "fallen"


class TypeRepeat(Enum):
    linear = "linear"
    manual = "manual"
    expo = "expo"
    log = "log"
    fibo = "fibo"
    evenly = "evenly"


class RepeatSchemas(Enum):
    attempts = "attempts"
    time = "time"


class TaskSchemas(BaseModel):
    """
    :: repeat_schemas :: - According to what principle we do repetitions -
                           by number of repetitions or to a specified time
    :: type_repeat :: - Delay scheme before repeats
    :: queue_sequence :: - If after a task has been completed in a queue,
                           it has to be forwarded on, we pass a list of
                           the list of queues, and in the process of execution,
                           the worker will look in which queue we are already
                           and if the task (task) is executed successfully,
                           it is forwarded to a new queue
    :: attempts :: - Number of attempts before the task gets to the sump
                    in case of failure
    :: counter :: - Attempts counter
    :: warning_attempts :: - If you want to inform that the task is badly
                             executed, but is still executing.
                             indicate on which attempt this is done
    :: expiry :: - If you set repeat_schemas=time - the task expiration time
    :: uuid_task :: - I see
    :: target_queue :: - Target queue where we get after a delay
    :: handler :: - Primary handler of the task
    :: sub_handler :: - Secondary task handler
    :: payload :: - Useful data for task processing. Any format.
    """
    repeat_schemas: str = str(RepeatSchemas.attempts.value)
    type_repeat: str = str(TypeRepeat.evenly.value)
    queue_sequence: dict = None
    attempts: int = 50
    counter: int = 0
    warning_attempts: int = 3
    expiry: str = str(datetime.now() + timedelta(hours=3))
    uuid_task: str
    target_queue: str
    handler: str = None
    sub_handler: str = None
    payload: dict | Any = None

    def set_expiry(self, time_delta: int = 60*60):
        delta = datetime.now() + timedelta(seconds=time_delta)
        self.expiry = delta.isoformat()

    def inc_counter(self):
        self.counter = self.counter + 1


class PayloadItem(BaseModel):
    text: str | list | dict
    item_type: str
    translated: bool = False
