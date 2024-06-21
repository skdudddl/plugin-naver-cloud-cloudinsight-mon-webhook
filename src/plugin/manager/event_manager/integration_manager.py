import logging
import json

from spaceone.core.utils import random_string

from plugin.manager.event_manager.base import ParseManager

_LOGGER = logging.getLogger("spaceone")


class IntegrationManager(ParseManager):
    webhook_type = "Integration"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data:
        :return EventResponse:
            "results": EventResponse
        """
        results = []

        _LOGGER.debug(f"[CloudInsight] parse => {json.dumps(raw_data, indent=2)}")

        #event_type_category = raw_data.get("detail", {}).get("eventTypeCategory", "")
        raw_data_text =raw_data.get("text")
        # raw_data = self.parse_text_to_dict(raw_data_text)

        event: dict = {
            'event_key': self.generate_event_key(raw_data),
            'event_type': self.get_event_type(raw_data),
            'severity': self.get_severity(raw_data),
            'resource': raw_data.get("resourceName"),#not required
            'title': self._change_string_format(raw_data),
            'rule': raw_data.get("ruleName"),#not required
            'description': raw_data_text,
            'occurred_at': self.convert_to_iso8601(raw_data.get("alarmStartTime")),
            'additional_info': self.get_additional_info(raw_data)
        }

        results.append(event)
        _LOGGER.debug(f"[Ncloud_Webhook] parse => {event}")

        return {
            "results": results
        }

    def generate_event_key(self, raw_data: dict) -> str:
        return random_string()

    def get_event_type(self, raw_data: dict) -> str:
        return "ALERT"

    def get_severity(self, raw_data: dict) -> str:
        if raw_data.get("eventLevel") is not None:
            return raw_data.get("eventLevel")
        else:
            return "INFO"

    @staticmethod
    def _change_string_format(raw_data):
        return raw_data.get("name")

    @staticmethod
    def get_additional_info(raw_data: dict) -> dict:
        additional_info = {
            "url": raw_data.get("url"),
            "dimension": raw_data.get("dimension", {})
        }

        return additional_info

    def parse_text_to_dict(self, text: str) -> dict:
        raw_data_dict = {}
        items = text.strip('{}').split(', ')
        print(items)
        for item in items:
            key, value = item.split(": ", 1)
            raw_data_dict[key.strip()] = value.strip()
        return raw_data_dict

