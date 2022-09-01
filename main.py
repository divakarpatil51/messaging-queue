import logging
import os

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

    consumer_A = JsonConsumer("A")
    # consumer_A.set_consumed_message_pattern(".*test*")
    in_mem_queue.subscribe(consumer=consumer_A)

    consumer_C = JsonConsumer("C")
    consumer_C.add_parent(consumer_A)
    # consumer_C.set_consumed_message_pattern(".*test*")
    in_mem_queue.subscribe(consumer=consumer_C)

    consumer_B = JsonConsumer("B")
    consumer_B.add_parent(consumer_C)
    consumer_B.add_parent(consumer_A)
    # _json_consumerB.set_consumed_message_pattern(".*abc*")
    in_mem_queue.subscribe(consumer=consumer_B)

    json_prod.produce(JsonMessage({"messageId": "test"}))

    json_prod.produce(JsonMessage({"messageId": "abc"}))

    json_prod.produce(JsonMessage({"messageId": "abc1"}))

    in_mem_queue.wait_for_tasks_execution()
