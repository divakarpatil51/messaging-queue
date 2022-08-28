from exceptions.queue_overflow_exception import QueueOverflowException
from models.message import Message
from utils.fifo_queue import FIFOQueue
from .message_queue import MessageQueue
import logging


class InMemoryMessageQueue(MessageQueue):

    def __init__(self, queue_size: int):
        self._consumers = []
        self._queue_size = queue_size
        self._messages = FIFOQueue()

    def subscribe(self, consumer):
        self._consumers.append(consumer)

    def publish(self, message: Message):
        self._validate_queue_size()
        self._messages.push(message=message)
        message = self._messages.pop()
        logging.info(f"New message {message.get_message()} added to the queue, Queue size: {len(self._consumers)}")
        for consumer in self._consumers:
            consumer.consume(message=message)

    def _validate_queue_size(self):
        if self._messages.size() == self._queue_size:
            raise QueueOverflowException("Queue is full, cannot add more messages to the queue")
