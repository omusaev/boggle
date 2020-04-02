import typing

from contextlib import contextmanager

from kombu import (
    Consumer, Producer, uuid, Queue,
    Message, Connection, Exchange
)
from kombu.pools import connections

from core.utils.logging import get_or_generate_request_id

from logging import getLogger

logger = getLogger(__name__)


class AsyncTaskProducer:
    """
    Base class for task producers
    """
    correlation_id = None

    def __init__(self, broker_url: str, exchange: Exchange,
                 routing_key: str = None,
                 callback_queue: typing.Optional[Queue] = None):
        self.broker_url = broker_url
        self.exchange = exchange
        self.routing_key = routing_key
        self.callback_queue = callback_queue

    @contextmanager
    def conn(self):
        with connections[Connection(self.broker_url)].acquire(block=True) as c:
            yield c

    def send(self, data: dict, routing_key: str = None,
             correlation_id: typing.Optional[str] = None,
             to_declare: typing.List[Queue] = None,
             auto_declare_queues: bool = False,
             auto_delete_queues: bool = False,
             expires: int = 86400,
             message_ttl: int = None):

        self.correlation_id = correlation_id or uuid()
        routing_key = routing_key or self.routing_key
        declare = to_declare if to_declare is not None else []

        kwargs = {
            'exchange': self.exchange,
            'routing_key': routing_key,
            'correlation_id': self.correlation_id,
            'headers': {'request_id': get_or_generate_request_id()},
            'declare': declare,
            'expiration': message_ttl
        }

        if auto_declare_queues:
            '''
                auto_delete:
                If set, the queue is deleted when all consumers have finished
                using it. Last consumer can be canceled either explicitly or
                because its channel is closed. If there was no consumer ever
                on the queue, it won’t be deleted.
            '''

            queue_kwargs = {
                'exchange': self.exchange,
                'routing_key': routing_key,
                'durable': True,
            }

            if auto_delete_queues:
                queue_kwargs.update({
                    'auto_delete': True,
                    'expires': expires
                })

            queue = Queue(
                routing_key,
                **queue_kwargs
            )
            declare.append(queue)

        if self.callback_queue:
            declare.append(self.callback_queue)
            kwargs.update({
                'reply_to': self.callback_queue.name,
            })

        with self.conn() as connection:
            with Producer(connection) as producer:
                logger.debug(
                    'Sending a message ({}). Data: {}, properties: {}'.format(
                        routing_key, data, kwargs))

                producer.publish(data, **kwargs)


# There are a few convenient mixins we could use (ConsumerMixin,
# ConsumerProducerMixin)
# but here we want to get a response and return it to the calling code instead
# of infinite consume loop1
# that's why here Consumer and Producer classes are used directly
class SyncTaskProducer(AsyncTaskProducer):
    """
    Creates a task and waits for a response in synchronous manner
    """

    response = None
    correlation_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.callback_queue is None:
            # this is a one time queue to get a result back in synchronous
            # manner
            # as soon as the connection is closed the queue will be deleted
            exchange = self.exchange
            routing_key = uuid()
            self.callback_queue = Queue(
                routing_key,
                exchange=exchange,
                routing_key=routing_key,
                auto_delete=True,
                expires=60 * 20,
            )

    def on_response(self, message: Message):
        # check correlation Id just in case something went wrong and we got a
        # wrong response
        if message.properties['correlation_id'] == self.correlation_id:
            self.response = message.payload
            logger.debug(
                'Got a response for task with correlation_id {}: {}'.format(
                    self.correlation_id, self.response))
            message.ack()
        else:
            logger.error('Expected a message with correlation id {},'
                         ' got {} instead. Message: {}, payload'.format(
                            self.correlation_id,
                            message.properties['correlation_id'],
                            message, message.payload))

    def send(self, *args, timeout=60 * 5, **kwargs):
        with self.conn() as connection:
            with Consumer(
                    connection,
                    on_message=self.on_response,
                    queues=[self.callback_queue]):

                super().send(*args, **kwargs)

                logger.debug('Waiting synchronously for a response for task'
                             ' with correlation id {}'.format(
                                self.correlation_id))

                while self.response is None:
                    # set timeout to avoid dead locks
                    connection.drain_events(timeout=timeout)

        return self.response
