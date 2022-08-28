from abc import ABC, abstractmethod


class Producer(ABC):

    @abstractmethod
    def produce(self, message):
        raise NotImplementedError("Method not implemented")
