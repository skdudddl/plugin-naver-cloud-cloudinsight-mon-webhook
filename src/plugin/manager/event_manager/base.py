import logging
from datetime import datetime
from typing import Union
from abc import abstractmethod, ABCMeta

from spaceone.core.manager import BaseManager
from plugin.error import *

__all__ = ['ParseManager']
_LOGGER = logging.getLogger('spaceone')


class ParseManager(BaseManager, metaclass=ABCMeta):

    webhook_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    @abstractmethod
    def parse(self, **kwargs):
        pass

    @abstractmethod
    def generate_event_key(self, **kwargs):
        pass

    @abstractmethod
    def get_event_type(self, event_state):
        pass

    @abstractmethod
    def get_severity(self, event_state):
        pass

    @abstractmethod
    def get_additional_info(self, *args, **kwargs):
        pass

    @classmethod
    def get_parse_manager_by_webhook_type(cls, webhook_type):
        for subclass in cls.__subclasses__():
            if subclass.webhook_type == webhook_type:
                return subclass()
        raise ERROR_INVALID_WEBHOOK_TYPE(webhook_type=webhook_type)

    @staticmethod
    def convert_to_iso8601(timestamp: int) -> Union[str, None]:
        if timestamp is not None:
            timestamp_in_seconds = timestamp / 1000.0
            dt = datetime.utcfromtimestamp(timestamp_in_seconds)
            return dt.isoformat() + 'Z'
        else:
            return "Undefined"

