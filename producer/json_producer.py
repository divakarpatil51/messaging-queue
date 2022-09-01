import logging

from exceptions.queue_overflow_exception import QueueOverflowException
from message_queue.message_queue import MessageQueue
from models.message import Message
from .producer import Producer


class JsonProducer(Producer):

    def __init__(self, queue: MessageQueue):
        self._queue = queue

    def produce(self, message: Message):
        retrial = 3
        while retrial > 0:
            try:
                self._queue.publish(message)
                break
            except QueueOverflowException:
                # Queue is full. Wait for sometime.
                ...
            except Exception:
                retrial -= 1
                if retrial == 0:
                    logging.info(f"Error occurred while publishing message: {message}")
                    break
