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

        event: dict = {
            'event_key': raw_data.get("productKey"),
            'event_type': self.get_event_status(raw_data),
            'severity': self.get_severity(raw_data),
            'resource': self.get_resource(raw_data),#not required
            'title': raw_data.get("ruleName", "[Ncloud]"),
            'rule': raw_data.get("ruleName"),#not required
            'description': raw_data.get("text"),
            'occurred_at': self.convert_to_iso8601(raw_data.get("alarmStartTime")),
            'additional_info': self.get_additional_info(raw_data)
        }

        results.append(event)
        _LOGGER.debug(f"[Ncloud_Webhook] parse => {event}")

        return {
            "results": results
        }

    @staticmethod
    def get_event_status(raw_data: dict) -> str:
        event_status = raw_data.get("eventStatus")
        if event_status == "RESOLVE":
            return "RECOVERY"
        else:
            return "ALERT"

    def get_severity(self, raw_data: dict) -> str:
        severity = raw_data.get("level")
        if severity is not None:
            return severity
        else:
            return "INFO"

    @staticmethod
    def get_resource(raw_data: dict) -> dict:
        return {
            "name": raw_data.get("resourceName"),
            "domain_code": raw_data.get("domainCode"),
            "region_code": raw_data.get("regionCode"),
            "dimensions": raw_data.get("dimensions")
        }

    def get_additional_info(self, raw_data: dict) -> dict:
        additional_info = {
            "rule_id": raw_data.get("ruleId"),
            "data_time": self.convert_to_iso8601(raw_data.get("dataTime")),
            "operator": raw_data.get("operator"),
            "metric": raw_data.get("metric"),
            "criteria": raw_data.get("criteria"),
            "duration": raw_data.get("duration"),
            "alarm_start_time": self.convert_to_iso8601(raw_data.get("alarmStartTime")),
            "alarm_end_time": self.convert_to_iso8601(raw_data.get("alarmEndTime")),
            "event_cause_type": raw_data.get("eventCauseType"),
            "value": raw_data.get("value"),
            "current_value": raw_data.get("currentValue"),
            "event_status": raw_data.get("eventStatus")

        }

        return additional_info



