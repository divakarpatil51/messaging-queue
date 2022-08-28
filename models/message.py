from abc import ABC, abstractmethod


class Message(ABC):

    @abstractmethod
    def get_message(self):
        raise NotImplementedError("Method not Implemented")

    def set_enqueue_time(self, enqueue_time: int):
        raise NotImplementedError("Method not Implemented")

    def get_enqueue_time(self):
        raise NotImplementedError("Method not Implemented")
