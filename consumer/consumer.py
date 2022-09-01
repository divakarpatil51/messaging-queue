from abc import ABC, abstractmethod
from typing import Set


class Consumer(ABC):

    def __init__(self, name):
        self._name = name
        # Setting default message pattern to match all text
        self._message_pattern = "."
        self._parents: Set[Consumer] = set()

    @abstractmethod
    def consume(self, message):
        raise NotImplementedError("Method not implemented")

    def get_name(self):
        return self._name

    def set_consumed_message_pattern(self, pattern: str):
        self._message_pattern = pattern

    def get_consumed_message_pattern(self):
        return self._message_pattern

    def add_parent(self, parent):
        self._parents.add(parent)

    def set_parents(self, parents: Set):
        self._parents = parents

    def get_parents(self):
        return self._parents

    def __str__(self):
        return f"Consumer Name: {self.get_name()}"

    __repr__ = __str__
