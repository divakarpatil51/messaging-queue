from abc import ABC, abstractmethod


class Consumer(ABC):

    def __init__(self, name):
        self._name = name
        # Setting default message pattern to match all text
        self._message_pattern = "."

    @abstractmethod
    def consume(self, message):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def set_consumed_message_pattern(self, pattern: str):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_consumed_message_pattern(self):
        raise NotImplementedError("Method not implemented")
