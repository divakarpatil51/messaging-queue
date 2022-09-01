from typing import Dict

from .message import Message


class JsonMessage(Message):

    def __init__(self, message: Dict):
        super(JsonMessage, self).__init__()
        if not isinstance(message, dict):
            raise Exception(f"Message expected to be of type dict but got {type(message)}")
        self._message = message
        self._enqueue_time = 0

    def get_message(self):
        return self._message

    def set_enqueue_time(self, enqueue_time: int):
        self._enqueue_time = enqueue_time

    def get_enqueue_time(self):
        return self._enqueue_time

    def __str__(self):
        return str(self._message)
