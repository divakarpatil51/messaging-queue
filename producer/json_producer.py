import time

from .producer import Producer
from message_queue.message_queue import MessageQueue
from exceptions.queue_overflow_exception import QueueOverflowException


class JsonProducer(Producer):

    def __init__(self, queue: MessageQueue):
        self._queue = queue

    def produce(self, message):
        while True:
            try:
                self._queue.publish(message)
                break
            except QueueOverflowException:
                # Queue is full. Wait for sometime.
                time.sleep(3)
