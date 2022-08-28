from .consumer import Consumer
from models.message import Message
import logging


class JsonConsumer(Consumer):

    def __init__(self, name):
        self._name = name

    def consume(self, message: Message):
        logging.info(f"Consumer {self._name} consumed the message: {message.get_message()}")
