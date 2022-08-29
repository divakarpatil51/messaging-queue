import logging
import time
from concurrent.futures import ThreadPoolExecutor

from exceptions.queue_overflow_exception import QueueOverflowException
from models.message import Message
from utils.fifo_queue import FIFOQueue
from utils.pattern_matcher import PatternMatcher
from .message_queue import MessageQueue


class InMemoryMessageQueue(MessageQueue):

    # TODO: Add message_ttl to config file
    def __init__(self, queue_size: int, message_ttl: int = 60):
        self._consumers = []
        self._queue_size = queue_size
        self._messages = FIFOQueue()
        # This value is in seconds
        self._message_ttl = message_ttl
        self._workers = 3
        self._in_progress_tasks = []
        self._executor = ThreadPoolExecutor(max_workers=self._workers)

    def subscribe(self, consumer):
        self._consumers.append(consumer)

    def publish(self, message: Message):
        self._validate_queue_size()
        message.set_enqueue_time(int(time.time()))
        self._messages.push(message=message)

        logging.info(f"New message {message.get_message()} added to the queue, Queue size: {self._messages.size()}")

        future = self._executor.submit(self._publish)
        self._in_progress_tasks.append(future)

    def _publish(self):
        message = self._messages.pop()
        if not self._has_msg_expired(message):
            for consumer in self._consumers:
                pattern = consumer.get_consumed_message_pattern()
                if PatternMatcher.match(pattern, str(message.get_message())):
                    consumer.consume(message=message)

    def wait_for_tasks_execution(self):
        while True:
            if all(list(map(lambda future: future.done(), self._in_progress_tasks))):
                logging.info("All messages consumed successfully")
                break

    def _validate_queue_size(self):
        if self._messages.size() == self._queue_size:
            logging.error("Queue is full, cannot add more messages to the queue")
            raise QueueOverflowException("Queue is full, cannot add more messages to the queue")

    def _has_msg_expired(self, message: Message):
        curr_time = int(time.time())
        if (curr_time - message.get_enqueue_time()) > self._message_ttl:
            logging.info(f"{message.get_message()} has expired.")
            return True
        return False
