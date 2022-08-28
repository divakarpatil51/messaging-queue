import logging

from models.message import Message
from .consumer import Consumer


class JsonConsumer(Consumer):

    def __init__(self, name):
        super(JsonConsumer, self).__init__(name=name)

    def consume(self, message: Message):
        logging.info(f"Consumer {self._name} consumed the message: {message.get_message()}")

    def set_consumed_message_pattern(self, pattern: str):
        self._message_pattern = pattern

    def get_consumed_message_pattern(self):
        return self._message_pattern
