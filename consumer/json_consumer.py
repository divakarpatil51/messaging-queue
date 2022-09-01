import logging

from models.message import Message
from .consumer import Consumer


class JsonConsumer(Consumer):

    def __init__(self, name):
        super(JsonConsumer, self).__init__(name=name)

    def consume(self, message: Message):
        logging.info(f"Consumer {self._name} consumed the message: {message.get_message()}")

    def __eq__(self, other):
        if isinstance(other, JsonConsumer):
            return self.get_name() == other.get_name()
        return False

    def __hash__(self):
        return hash(self.get_name())
