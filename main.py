from message_queue.in_memory_message_queue import InMemoryMessageQueue
from producer.json_producer import JsonProducer
from consumer.json_consumer import JsonConsumer

if __name__ == '__main__':
    in_mem_queue = InMemoryMessageQueue()
    json_prod = JsonProducer(in_mem_queue)
    _json_consumer = JsonConsumer("A")
    in_mem_queue.subscribe(consumer=_json_consumer)

    json_prod.produce({"test": "test"})


