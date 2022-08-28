from .producer import Producer
from message_queue.message_queue import MessageQueue


class JsonProducer(Producer):

    def __init__(self, queue: MessageQueue):
        self._queue = queue

    def produce(self, message):
        self._queue.publish(message)
