import logging
import json
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_webhook.connector.webhook_connector import WebhookConnector
from spaceone_webhook.manager.event_manager.base import ParseManager

_LOGGER = logging.getLogger("spaceone")


class CloudInsightManager(ParseManager):
    webhook_type = "Ncloud_CloudInsight"

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
            'event_type': self.get_event_type(""),
            'severity': self.get_severity(raw_data),
            'resource': self._get_resource(raw_data),#not required
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
        return raw_data.get("eventId")

    def get_event_type(self, event_state: str) -> str:
        return "ALERT"

    def get_severity(self, raw_data: dict) -> str:
        return raw_data.get("eventLevel")

    @staticmethod
    def _change_string_format(raw_data):
        event_title = raw_data.get("ruleName") + "-" +raw_data.get("metric")
        return event_title

    @staticmethod
    def get_additional_info(raw_data: dict) -> dict:
        additional_info = {
            'rule_id' : raw_data.get("ruleId"),
            "prod_key": raw_data.get("prodKey"),
            'product_name': raw_data.get("prodName"),
            'metric': raw_data.get("metric"),
            'detect_value': raw_data.get("detectValue"),
            'notification_groups': raw_data.get("notificationGroups"),
            "criteria" : raw_data.get("criteria")
        }
        dimension = raw_data.get("dimension", {})
        for key, value in dimension.items():
            additional_info[f'{key}'] = value

        return additional_info

    @staticmethod
    def _get_resource(raw_data: dict) -> dict:
        return {
            "name": raw_data.get("resourceName")
        }
