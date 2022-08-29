import logging
import os
import time

from consumer.json_consumer import JsonConsumer
from message_queue.in_memory_message_queue import InMemoryMessageQueue
from models.json_message import JsonMessage
from producer.json_producer import JsonProducer
from utils.logger import LoggerConfig, LogHandlerType

DEFAULT_QUEUE_SIZE = 3
LoggerConfig.create_logger(log_type=LogHandlerType.StreamHandler)

if __name__ == '__main__':

    queue_size = os.getenv("queue_size", DEFAULT_QUEUE_SIZE)

    logging.info(f"Creating queue with size: {queue_size}")
    in_mem_queue = InMemoryMessageQueue(queue_size=queue_size)

    json_prod = JsonProducer(in_mem_queue)

    _json_consumer = JsonConsumer("A")
    _json_consumer.set_consumed_message_pattern(".*test*")

    _json_consumerB = JsonConsumer("B")
    # _json_consumerB.set_consumed_message_pattern(".*abc*")

    in_mem_queue.subscribe(consumer=_json_consumer)
    in_mem_queue.subscribe(consumer=_json_consumerB)

    message = JsonMessage({"messageId": "test"})
    json_prod.produce(message)

    message = JsonMessage({"messageId": "abc"})
    json_prod.produce(message)

    message = JsonMessage({"messageId": "abc1"})
    json_prod.produce(message)

    in_mem_queue.wait_for_tasks_execution()
