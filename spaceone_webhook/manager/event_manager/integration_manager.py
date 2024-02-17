import logging
import json
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_webhook.manager.event_manager.base import ParseManager

_LOGGER = logging.getLogger("spaceone")


class IntegrationManager(ParseManager):
    webhook_type = "Ncloud_Integration"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data:
        :return EventResponse:
            "results": EventResponse
        """
        results = []

        _LOGGER.debug(f"[AWSPersonalHealthDashboard] parse => {json.dumps(raw_data, indent=2)}")

        #event_type_category = raw_data.get("detail", {}).get("eventTypeCategory", "")

        event: dict = {
            'event_key': self.generate_event_key(raw_data),
            'event_type': self.get_event_type(raw_data),
            'severity': self.get_severity(raw_data),
            #'resource': self._get_resource(raw_data),#not required
            'title': self._change_string_format(raw_data),
            'rule': raw_data.get("ruleName"),#not required
            'occurred_at': self.convert_to_iso8601(raw_data.get("startTime")),
            'additional_info': self.get_additional_info(raw_data)
        }

        results.append(event)
        _LOGGER.debug(f"[Ncloud_Webhook] parse => {event}")

        return {
            "results": results
        }

    def generate_event_key(self, raw_data: dict) -> str:
        return raw_data.get("id")

    def get_event_type(self, raw_data: dict) -> str:
        return raw_data.get("type")

    def get_severity(self, raw_data: dict) -> str:
        if raw_data.get("eventLevel") is not None:
            return raw_data.get("eventLevel")
        else :
            return "UNKNOWN"

    @staticmethod
    def _change_string_format(raw_data):
        return raw_data.get("name")

    @staticmethod
    def get_additional_info(raw_data: dict) -> dict:
        all_keys = [
            "DOMAIN_CODE", "REGION_CODE", "PRODUCT_KEY", "PRODUCT_NAME",
            "RESOURCE_NAME", "DIMENSIONS", "RULE_ID", "RULE_NAME", "DATA_TIME",
            "LEVEL", "OPERATOR", "METRIC", "UNIT", "AGGREGATION_METHOD",
            "CRITERIA", "DURATION", "ALARM_START_TIME", "ALARM_END_TIME",
            "EVENT_CAUSE_TYPE", "VALUE", "CURRENT_VALUE", "EVENT_STATUS"
        ]

        additional_info = {}

        if "DIMENSIONS" in raw_data and raw_data.get("DIMENSIONS"):
            try:
                dimensions = raw_data["DIMENSIONS"]
                additional_info["DIMENSIONS"] = dimensions
            except json.JSONDecodeError:
                additional_info["DIMENSIONS"] = raw_data["DIMENSIONS"]

        for key in all_keys:
            if key in raw_data and key != "DIMENSIONS":
                additional_info[key] = raw_data[key]

        return additional_info


    @staticmethod
    def _get_resource(raw_data: dict) -> dict:
        return {
            "name": raw_data.get("resourceName")
        }
