from message_queue.in_memory_message_queue import InMemoryMessageQueue
from producer.json_producer import JsonProducer
from consumer.json_consumer import JsonConsumer
from models.json_message import JsonMessage
import os

DEFAULT_QUEUE_SIZE = 3

if __name__ == '__main__':
    queue_size = os.getenv("queue_size", DEFAULT_QUEUE_SIZE)
    print(f"Creating queue with size: {queue_size}")
    in_mem_queue = InMemoryMessageQueue(queue_size=queue_size)

    json_prod = JsonProducer(in_mem_queue)

    _json_consumer = JsonConsumer("A")
    in_mem_queue.subscribe(consumer=_json_consumer)

    message = JsonMessage({"messageId": "test"})
    json_prod.produce(message)
