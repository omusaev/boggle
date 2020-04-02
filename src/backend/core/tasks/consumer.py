from kombu import Connection, Queue, Message
from kombu.mixins import ConsumerProducerMixin

from core.utils.logging import (
    set_request_id, generate_request_id, get_request_id
)

from logging import getLogger

logger = getLogger(__name__)


class BaseConsumer(ConsumerProducerMixin):

    def __init__(self, broker_url, queue: Queue):
        self._broker_url = broker_url
        self.connection = Connection(broker_url)
        self.queue = queue
        self.exchange = queue.exchange

    def get_consumers(self, Consumer, channel):
        # prefetch_count:
        # The client can request that messages should be sent in advance
        # so that when the client finishes processing a message, the following
        # message is already held locally, rather than needing to be sent down
        # the channel. Prefetching gives a performance improvement.
        return [Consumer(
            queues=[self.queue],
            on_message=self.on_request,
            accept={'application/json'},
            prefetch_count=1,
        )]

    def on_request(self, message: Message):
        self._set_request_id(message)

        logger.debug('{}: Got a new message: {}, payload: {}'.format(
            self.__class__.__name__, message.properties, message.payload))

        result = self.process_message(message)

        logger.debug('{}: Finished task with correlation_id {}. Result: {}'.
                     format(self.__class__.__name__,
                            message.properties['correlation_id'], result)
        )

        message.ack()

        if 'reply_to' in message.properties:
            logger.debug(
                '{}: Sending a result: {}, exchange: {}, routing_key:'' {},'
                ' correlation_id: {}'.format(
                        self.__class__.__name__,
                        result, self.exchange, message.properties['reply_to'],
                        message.properties['correlation_id'])
            )
            self.producer.publish(
                result,
                exchange=self.exchange,
                routing_key=message.properties['reply_to'],
                correlation_id=message.properties['correlation_id'],
                request_id=self._get_request_id(),
                serializer='json',
                retry=True,
            )

    def process_message(self, message: Message):
        raise NotImplementedError

    def _set_request_id(self, message):
        request_id = message.headers.get(
            'request_id', generate_request_id())

        set_request_id(request_id)

    def _get_request_id(self):
        return get_request_id()
