import logging
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Set

from consumer.consumer import Consumer
from exceptions.queue_overflow_exception import QueueOverflowException
from models.message import Message
from utils.fifo_queue import FIFOQueue
from utils.pattern_matcher import PatternMatcher
from .message_queue import MessageQueue
from .dead_letter_queue import DeadLetterQueue


class InMemoryMessageQueue(MessageQueue):

    # TODO: Add message_ttl to config file
    def __init__(self, queue_size: int, message_ttl: int = 60):
        self._consumers: Set[Consumer] = set()
        self._queue_size = queue_size
        self._messages = FIFOQueue()
        # This value is in seconds
        self._message_ttl = message_ttl
        self._workers = 3
        self._in_progress_tasks = []
        self._executor = ThreadPoolExecutor(max_workers=self._workers)
        self._lock = Lock()
        self._dlq = DeadLetterQueue(self)

    def subscribe(self, consumer: Consumer):
        self._validate_consumer_lineage(consumer)
        self._consumers.add(consumer)

    def _validate_consumer_lineage(self, consumer: Consumer):
        parents = consumer.get_parents()
        if parents and not parents.issubset(self._consumers):
            missing = parents.difference(self._consumers)
            raise Exception(f"Consumers with name {missing} not subscribed to the queue")

    def publish(self, message: Message):
        self._validate_queue_size()
        message.set_enqueue_time(int(time.time()))
        self._messages.push(message=message)

        logging.info(f"New message {message.get_message()} added to the queue, Queue size: {self._messages.size()}")

        future = self._executor.submit(self._publish)
        self._in_progress_tasks.append(future)

    def _publish(self):
        with self._lock:
            message = self._messages.pop()
        if not self._has_msg_expired(message):
            consumers_stack = []
            consumers_visited = []
            for consumer in self._consumers:
                pattern = consumer.get_consumed_message_pattern()

                if not PatternMatcher.match(pattern, str(message.get_message())) \
                        or consumer in consumers_visited:
                    continue

                parents = consumer.get_parents()
                consumers_stack.append(consumer)
                if parents:
                    consumers_stack.extend(parents)
                while consumers_stack:
                    curr_consumer = consumers_stack.pop()
                    if curr_consumer in consumers_visited:
                        continue
                    curr_consumer_pattern = curr_consumer.get_consumed_message_pattern()
                    if PatternMatcher.match(curr_consumer_pattern, str(message.get_message())):
                        self._process_consume(consumer=curr_consumer, message=message)
                        consumers_visited.append(curr_consumer)

    def _process_consume(self, consumer: Consumer, message: Message):
        while message.get_retry_count() > 0:
            try:
                consumer.consume(message=message)
                break
            except Exception:
                message.set_retry_count(message.get_retry_count() - 1)
        else:
            logging.info(f"Error occurred while consuming message: {message}. Adding it to Dead letter queue.")
            self._dlq.put(message=message)

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

    def get_dlq(self):
        return self._dlq
