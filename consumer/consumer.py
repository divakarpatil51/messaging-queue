from abc import ABC, abstractmethod


class Consumer(ABC):

    @abstractmethod
    def consume(self, message):
        raise NotImplementedError("Method not implemented")
