from .message_queue import MessageQueue
from models.message import Message


class InMemoryMessageQueue(MessageQueue):

    def __init__(self):
        self._consumers = []

    def subscribe(self, consumer):
        self._consumers.append(consumer)

    def publish(self, message: Message):
        print(f"New message {message.get_message()} added to the queue, Queue size: {len(self._consumers)}")
        for consumer in self._consumers:
            consumer.consume(message=message)
