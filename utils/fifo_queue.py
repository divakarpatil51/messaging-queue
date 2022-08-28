from collections import deque

from models.message import Message
from .queue import Queue


class FIFOQueue(Queue):

    def __init__(self):
        self._queue = deque()

    def push(self, message: Message):
        self._queue.append(message)

    def pop(self) -> Message:
        return self._queue.popleft()

    def peek(self):
        return self._queue[0]

    def size(self):
        return len(self._queue)

    def is_empty(self):
        return not self._queue
