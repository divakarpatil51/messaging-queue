import logging

from models.message import Message
from utils.fifo_queue import FIFOQueue
from .message_queue import MessageQueue


class DeadLetterQueue:

    def __init__(self, source_queue: MessageQueue):
        self._messages = FIFOQueue()
        self._source_queue = source_queue
        self.count = 10

    def put(self, message: Message):
        self._messages.push(message)

    def process_messages(self):
        while not self._messages.is_empty():
            message = self._messages.pop()
            logging.info("DLQ processing message --> ", message)
            try:
                self._source_queue.publish(message=message)
            except Exception:
                break
