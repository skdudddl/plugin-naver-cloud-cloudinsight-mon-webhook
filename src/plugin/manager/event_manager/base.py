import logging
from datetime import datetime
from typing import Union
from abc import abstractmethod, ABCMeta

from spaceone.core.manager import BaseManager
from spaceone.core.utils import datetime_to_iso8601

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
    def convert_to_iso8601(timestamp: Union[str, int, None]) -> Union[str, None]:
        if timestamp is not None:
            try:
                # Convert to integer if it's a string
                if isinstance(timestamp, str):
                    timestamp = int(timestamp)
                timestamp_in_seconds = timestamp / 1000.0
                dt = datetime.utcfromtimestamp(timestamp_in_seconds)
                return datetime_to_iso8601(dt)
            except (ValueError, TypeError) as e:
                _LOGGER.error(f"Error converting timestamp: {e}")
                return datetime_to_iso8601(datetime.now())
        else:
            return datetime_to_iso8601(datetime.now())
