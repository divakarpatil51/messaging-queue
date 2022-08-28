from .consumer import Consumer


class JsonConsumer(Consumer):

    def __init__(self, name):
        self._name = name

    def consume(self, message):
        print(f"Consumer {self._name} consumed the message: {message}")
