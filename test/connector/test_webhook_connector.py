import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

from spaceone_webhook.connector.webhook_connector import WebhookConnector
_LOGGER = logging.getLogger(__name__)


class TestServerConnector(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})
    keys = global_config.get("KEYS", {})
    pages = global_config.get("PAGES", {})


    webhook_connector = WebhookConnector(secret_data=secrets, prod_key=keys, page_data = pages)

    def test_list_webhook_instance(self):
        webhook_client = self.webhook_connector.list_metrics_group()

        print(webhook_client)
