import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

from spaceone_webhook.manager.event_manager.webhook_manager import WebhookManager

_LOGGER = logging.getLogger(__name__)


class TestWebhookManager(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})
    keys = global_config.get("KEYS", {})
    pages = global_config.get("PAGES", {})

    webhook_manager = WebhookManager(secret_data=secrets, prod_key= keys, page_data=pages)
    webhook_instances = webhook_manager.parse(options={}, secret_data=secrets, prod_key= keys, page_data = pages)

    for webhook_instance in webhook_instances:
        print(webhook_instance)

