import os
import signal
import sys

from conf import settings
from core.models.database import init_db
from core.tasks.config import start_handler, init_tasks


def signal_handler(sig, frame):
    sys.exit(0)


def start():
    handler_name = os.getenv('HANDLER_NAME')

    if not handler_name:
        raise Exception('HANDLER_NAME is required')

    init_db(settings.DATABASE)
    init_tasks(settings.TASKS_BROKER_URL)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    start_handler(handler_name)


if __name__ == '__main__':
    print('...Press ctrl+c to exit...')
    start()
