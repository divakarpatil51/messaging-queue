from abc import ABC, abstractmethod

from models.message import Message


class Queue(ABC):

    @abstractmethod
    def push(self, message: Message):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def pop(self) -> Message:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def peek(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def size(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def is_empty(self):
        raise NotImplementedError("Method not implemented")
