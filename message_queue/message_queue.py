from abc import ABC, abstractmethod


class MessageQueue(ABC):

    @abstractmethod
    def subscribe(self, consumer):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def publish(self, message):
        raise NotImplementedError("Method not implemented")
