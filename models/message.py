from abc import ABC, abstractmethod


class Message(ABC):

    def __init__(self, retry_count=3):
        self._retry_count = retry_count

    @abstractmethod
    def get_message(self):
        raise NotImplementedError("Method not Implemented")

    def set_enqueue_time(self, enqueue_time: int):
        raise NotImplementedError("Method not Implemented")

    def get_enqueue_time(self):
        raise NotImplementedError("Method not Implemented")

    def get_retry_count(self):
        return self._retry_count

    def set_retry_count(self, retry_count):
        self._retry_count = retry_count
