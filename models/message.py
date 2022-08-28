from abc import ABC, abstractmethod


class Message(ABC):

    @abstractmethod
    def get_message(self):
        raise NotImplementedError("Method not Implemented")
