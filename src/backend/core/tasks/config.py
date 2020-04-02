"""
    from core.tasks.config import get_task_manager

    task_manager = get_task_manager()

    # sync call
    result = task_manager.sync_task(TaskType.deploy).send({'test': 'test'})

    # async call
    # if 'callback_queue' in TASKS is None, target_queue handler will not send
    # a response back
    task_manager.async_task(TaskType.deploy).send({'test': 'test'})
"""
from kombu import Exchange, Queue, Connection

from apps.boggle.jobs.solver import BoggleSolverJob

from logging import getLogger


logger = getLogger(__name__)


class TaskTypes:
    SOLVE_BOGGLE = 'solve_boggle'


_broker_url = None
exchange = Exchange('tasks', type='direct', durable=True)

QUEUES = {
    'solve_boggle': Queue(
        'solve_boggle',
        exchange,
        routing_key='solve_boggle',
        durable=True),
}

HANDLERS = {
    'boggle_solver': {
        'queue': QUEUES['solve_boggle'],
        'handler_cls': BoggleSolverJob,
    },
}

TASKS = {
    TaskTypes.SOLVE_BOGGLE: {
        'exchange': QUEUES['solve_boggle'].exchange,
        'routing_key': QUEUES['solve_boggle'].routing_key,
        'callback_queue': None,
    },
}


def init_tasks(broker_url: str):
    global _broker_url
    _broker_url = broker_url

    # declare exchanges explicitly here
    # because if it's not used with a queue it will not be
    # automatically created
    with Connection(_broker_url, heartbeat=0) as c:
        c.connect()
        channel = c.channel()
        exchange(channel=channel).declare()


def start_handler(handler_name):
    handler_config = HANDLERS[handler_name]

    queue = handler_config.get('queue')
    if queue:
        handler = handler_config['handler_cls'](
            broker_url=_broker_url,
            queue=queue
        )
    else:
        handler = handler_config['handler_cls']()

    handler.run()


def get_task_manager():
    assert _broker_url is not None
    # import here to avoid circular import
    from core.tasks.manager import TaskManager

    return TaskManager(_broker_url, TASKS)
