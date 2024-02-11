from typing import List
import json
from spaceone.monitoring.plugin.webhook.lib.server import WebhookPluginServer
from spaceone_webhook.manager.event_manager.base import ParseManager
from spaceone_webhook.manager.event_manager.webhook_manager import WebhookManager
app = WebhookPluginServer()


@app.route("Webhook.init")
def webhook_init(params: dict) -> dict:
    """init plugin by options

    Args:
        params (WebhookInitRequest): {
            'options': 'dict'      # Required
        }

    Returns:
        WebhookResponse: {
            'metadata': 'dict'
        }
    """
    return {
        'meatadata': {}
    }


@app.route("Webhook.verify")
def webhook_verify(params: dict) -> None:
    """Verifying webhook plugin

    Args:
        params (WebhookVerityRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'schema': 'str',
            'domain_id': 'str'      # Required
        }

    Returns:
        None
    """
    pass


@app.route("Event.parse")
def event_parse(params: dict) -> List[dict]:
    """Parsing Event Webhook

    Args:
        params (EventRequest): {
            'options': 'dict',  # Required
            'data': 'dict'      # Required
        }

    Returns:
        List[EventResponse]
        {
            'event_key': 'str',         # Required
            'event_type': 'str',        # Required
            'title': 'str',
            'description': 'str',
            'severity': 'str',
            'resource': 'dict',
            'rule': 'str',              # Required
            'occurred_at': 'datetime',  # Required
            'additional_info': 'dict',
            'image_url': 'str'
        }
    """
    options = params["options"]
    data = params["data"]
    secret_data = params["options"].get("secret_data")
    prod_key = params["options"].get("prod_key")
    page_data = params["options"].get("page_data")
    #schema = params.get("schema")

    webhook_mgr = WebhookManager(secret_data=secret_data, prod_key=prod_key, page_data = page_data)
    return webhook_mgr.parse(options, secret_data, prod_key, page_data)

    # Check if webhook messages are SNS subscription
#     webhook_type = _get_webhook_type(data)
#     parse_mgr = ParseManager.get_parse_manager_by_webhook_type(webhook_type)
#
#     if webhook_type == "Ncloud_webhook":
#         return parse_mgr.parse(data)
#     else:
#         return parse_mgr.parse(json.loads(data.get("Message", "")))
#
#
# def _get_webhook_type(data: dict) -> str:
#     if data.get("Type") == "SubscriptionConfirmation":
#         return "Ncloud_webhook"
#     else:
#         return "AWS_CLOUDWATCH"
