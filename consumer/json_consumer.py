from .consumer import Consumer
from models.message import Message


class JsonConsumer(Consumer):

    def __init__(self, name):
        self._name = name

    def consume(self, message: Message):
        print(f"Consumer {self._name} consumed the message: {message.get_message()}")
