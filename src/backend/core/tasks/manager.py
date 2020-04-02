import typing

from core.tasks.producer import AsyncTaskProducer, SyncTaskProducer


class TaskManager:

    def __init__(self, broker_url: str,
                 tasks_config: typing.Dict[str, typing.Dict]):
        self.broker_url = broker_url
        self.tasks_config = tasks_config

    def sync_task(self, task_type) -> SyncTaskProducer:
        assert task_type in self.tasks_config

        config = self.tasks_config[task_type]

        if config.get('callback_queue') is not None:
            raise Exception('Task {} cannot be used in synchronous manner, '
                            'because there is a result handler for it.'.format(
                task_type)
            )

        # callback_queue is None to create a one-time queue instead of using a
        # durable queue, because it's safer
        # it's always a new queue, so there is no garbage messages inside
        producer = SyncTaskProducer(
            self.broker_url,
            exchange=config['exchange'],
            routing_key=config['routing_key'],
            callback_queue=None
        )

        return producer

    def async_task(self, task_type) -> AsyncTaskProducer:
        assert task_type in self.tasks_config

        config = self.tasks_config[task_type]
        # if callback_queue is None, task handler will not send a response
        producer = AsyncTaskProducer(
            self.broker_url,
            exchange=config['exchange'],
            routing_key=config['routing_key'],
            callback_queue=config.get('callback_queue')
        )

        return producer
