import logging
import os
from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict
from spaceone_webhook.manager.event_manager.webhook_manager import WebhookManager

_LOGGER = logging.getLogger(__name__)


class TestWebhook(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})
    keys = global_config.get("KEYS", {})
    pages = global_config.get("PAGES", {})



    def test_init(self):
        v_info = self.monitoring.Webhook.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        self.monitoring.Webhook.verify({'options': {}})


    def test_parse(self):
        cloudinsight_param = {

        }
        options = {}
        secret_data = self.secrets
        prod_key = self.keys
        page_data = self.pages
        webhook_manager = WebhookManager(secret_data=secret_data, prod_key=prod_key, page_data=page_data)
        # for webhook_instance in webhook_manager.parse(options={}, secret_data=secret_data, prod_key=prod_key, page_data=page_data, schema={}):
        #     params = {"options": options, "data": webhook_instance}
        #     parsed_data = self.monitoring.Event.parse(params)
        #     print_json(parsed_data)
        #     print()
        cloudinsight_pared_data = self.monitoring.Event.parse({'options': cloudinsight_param.get("options"), 'data': cloudinsight_param.get('data')})
        print_json(cloudinsight_pared_data)
        print()

