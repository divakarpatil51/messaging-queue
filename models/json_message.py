from .message import Message
from typing import Dict


class JsonMessage(Message):

    def __init__(self, message: Dict):
        if not isinstance(message, dict):
            raise Exception(f"Message expected to be of type dict but got {type(message)}")
        self._message = message

    def get_message(self):
        return self._message

    def __str__(self):
        return str(self._message)
