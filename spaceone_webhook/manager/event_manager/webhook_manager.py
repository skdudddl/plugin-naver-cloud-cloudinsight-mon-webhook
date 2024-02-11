import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_webhook.connector.webhook_connector import WebhookConnector

_LOGGER = logging.getLogger("spaceone")


class WebhookManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "SpaceONE"
        self.cloud_service_type = "Webhook"
        self.provider = "naver cloud"
        self.metadata_path = "metadata/spaceone/webhook.yaml"

    # def collect_resources(self, options, secret_data, prod_key, page_data, schema):
    #     try:
    #         yield from self.collect_cloud_service_type(options, secret_data, prod_key, page_data, schema)
    #         yield from self.collect_cloud_service(options, secret_data,  prod_key, page_data, schema)
    #     except Exception as e:
    #         yield make_error_response(
    #             error=e,
    #             provider=self.provider,
    #             cloud_service_group=self.cloud_service_group,
    #             cloud_service_type=self.cloud_service_type,
    #         )

    # def collect_cloud_service_type(self, options, secret_data,  prod_key, pages, schema):
    #     cloud_service_type = make_cloud_service_type(
    #         name=self.cloud_service_type,
    #         group=self.cloud_service_group,
    #         provider=self.provider,
    #         metadata_path=self.metadata_path,
    #         is_primary=True,
    #         is_major=True,
    #     )
    #
    #     yield make_response(
    #         cloud_service_type=cloud_service_type,
    #         match_keys=[["name", "reference.resource_id", "account", "provider"]],
    #         resource_type="monitoring.CloudServiceType",
    #     )

    def parse(self, options, secret_data, prod_key, page_data) -> list:
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

