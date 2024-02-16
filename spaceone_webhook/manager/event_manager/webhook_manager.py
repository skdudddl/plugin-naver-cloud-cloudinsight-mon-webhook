import logging
import json
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_webhook.connector.webhook_connector import WebhookConnector
from spaceone_webhook.manager.event_manager.base import ParseManager

_LOGGER = logging.getLogger("spaceone")


class WebhookManager(ParseManager):
    webhook_type = "Ncloud_CloudInsight"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data:
        :return EventResponse:
            "results": EventResponse
        """
        results = []

        _LOGGER.debug(f"[AWSPersonalHealthDashboard] parse => {json.dumps(raw_data, indent=2)}")

        event_type_category = raw_data.get("detail", {}).get("eventTypeCategory", "")

        event: dict = {
            'event_key': self.generate_event_key(raw_data),
            'event_type': self.get_event_type(""),
            'severity': self.get_severity(""),
            'resource': self._get_resource(raw_data),#not required
            'title': self._change_string_format(raw_data),
            'rule': event_type_category,#not required
            'occurred_at': self.convert_to_iso8601(raw_data.get("createTime")),
            'additional_info': self.get_additional_info(raw_data)
        }

        results.append(event)
        _LOGGER.debug(f"[Ncloud_Webhook] parse => {event}")

        return {
            "results": results
        }

    def generate_event_key(self, raw_data: dict) -> str:
        return raw_data.get("id")

    def get_event_type(self, event_state: str) -> str:
        return "ALERT"

    def get_severity(self, raw_: str) -> str:
        return "INFO"

    @staticmethod
    def _change_string_format(raw_data):
        return raw_data.get("groupName")

    @staticmethod

    def get_additional_info(self, raw_data: dict) -> dict:
        return {
            "prod_key" : raw_data.get("prodKey"),
            'product_name' : raw_data.get("productName"),
            "update_time" : self.convert_to_iso8601(raw_data.get("updateTime")),
            'region_code' : raw_data.get("regionCode")
        }

    @staticmethod
    def _get_resource(raw_data: dict) -> dict:
        return {
            "resource_id": raw_data.get("detail", {}).get("eventArn", ""),
            "resource_type": raw_data.get("source", "aws.health")
        }

    def parse11(self, options, secret_data, prod_key, page_data) -> list:
        results = []
        webhook_connector = WebhookConnector(secret_data=secret_data, prod_key=prod_key, page_data = page_data)
        webhook_instances = webhook_connector.list_metrics_group()
        for webhook_instance in webhook_instances:
            metrics_groups_data = get_metrics_groups(webhook_instance)
            monitor_groups_data = get_monitor_groups(webhook_instance)
            notifications_data = get_recipient_notifications_data(webhook_instance)
            details_data = get_rule_details_data(webhook_instance)
            webhook_data = {
                'metrics_groups': metrics_groups_data,
                'monitor_groups': monitor_groups_data,
                'notifications': notifications_data,
                'details': details_data


            }
            results.append(webhook_data)
            _LOGGER.debug(f"[Ncloud Webhook] parse => {webhook_data}")

        return results


def get_metrics_data(instance):
    metrics_data =[]
    for metric in instance['metrics'] :
        metric_data = {
            "calculation" : metric['calculation'],
            "condition" : metric['condition'],
            "duration" : metric['duration'],
            "event_level" : metric['eventLevel'],
            "desc" : metric.get('des',None),
            "metric" : metric['metric'],
            "metric_group_iItem_id" : metric['metricGroupItemId'],
            "threshold" : metric['threshold']
        }
        dimensions_data = [{'dim': dim['dim'], 'val': dim['val']} for dim in metric['dimensions']]
        metric_data['dimensions'] = dimensions_data
        metrics_data.append(metric_data)

    return metrics_data

def get_metrics_group_details_data(instance):
    metrics_group_details_data = {
        'create_time' : instance['createTime'],
        'domain_code' : instance['domainCode'],
        'group_name' : instance.get('groupName', None),
        'id' : instance['id'],
        'prod_key' : instance['prodKey'],
        'region_code' : instance['regionCode'],
        'update_time' : instance['updateTime']
    }
    return metrics_group_details_data

def get_metrics_groups(instance):
    metrics_groups_data = []
    for metrics_group in instance['metricsGroups']:
        metrics_data = get_metrics_data(metrics_group)
        metrics_group_details = get_metrics_group_details_data(metrics_group)
        metrics_groups_data.append({
            'metrics': metrics_data,
            'details': metrics_group_details
        })
    return metrics_groups_data

def get_monitor_group_item_data(instance):
    monitor_group_item_data =[]
    for item in instance['monitorGroupItemList'] :
        monitor_item_data = {
            'nrn' : item['nrn'],
            'resource_id' : item['resourceId']
        }
        monitor_group_item_data.append(monitor_item_data)

    return monitor_group_item_data

def get_recipient_notifications_data(instance):
    recipient_notifications_data =[]
    for notification in instance['recipientNotifications'] :
        notification_data = {
            'group_name' : notification['groupName'],
            'group_num' : notification['groupNum'],

        }
        notify_type_data = [notify for notify in notification['notifyTypes']]
        notification_data['notify_type'] = notify_type_data

        recipient_notifications_data.append(notification_data)

    return recipient_notifications_data
def get_monitor_group_details_data(instance):
    monitor_group_details_data = {
        'group_des' : instance.get('groupDes', None),
        'group_name' : instance.get('groupName', None),
        'id' : instance['id'],
        'prod_key' : instance['prodKey'],
        'temporary_group' : instance['temporaryGroup']
    }
    return monitor_group_details_data

def get_monitor_groups(instance):
    monitor_groups_data = []
    for monitor_group in instance['monitorGroups']:
        resource_data = get_monitor_group_item_data(monitor_group)
        monitor_group_details = get_monitor_group_details_data(monitor_group)
        monitor_groups_data.append({
            'resources': resource_data,
            'details': monitor_group_details
        })
    return monitor_groups_data

def get_rule_details_data(instance):
    rule_details_data = {
        'create_time' : instance['createTime'],
        'domain_code' : instance['domainCode'],
        'group_name' : instance['groupName'],
        'id' : instance['id'],
        'prod_key' : instance['prodKey'],
        'product_name' : instance['productName'],
        'region_code' : instance['regionCode'],
        'rule_version' : instance['ruleVersion'],
        'update_time' : instance['updateTime']
    }
    return rule_details_data

