import logging
import os
from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json


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
            "options": {},
            "data": {
              "events": {
                  "calc": "AVG",
                  "calcSlidingGroupKey": "",
                  "criteria": 0,
                  "detectValue": 0.7944445,
                  "dimension": {
                    "instanceNo": "xxxxxxx",
                    "type": "svr"
                  },
                  "endTime": 0,
                  "eventId": "xxxxxxxxxxxxxxxxxx",
                  "eventLevel": "INFO",
                  "metric": "avg_write_cnt",
                  "notificationGroups": "Recipient: NotiGrp001",
                  "operator": "GE",
                  "prodKey": "xxxxxxxxxxxxxxxxxx",
                  "prodName": "System/Server",
                  "resourceName": "svr-pub",
                  "ruleId": "xxxxxxxxxxxxxxxxxx",
                  "ruleName": "rule002",
                  "startTime": 1596088621223
                }
            }
        }

        integration_param = {
            "options": {},
            "data": {
              "headers": {
                "content-type": "application/json; charset=utf-8"
              },
              "id": "111",
              "name": "event test",
              "payload": "{\n\t\"text\": \"#{DOMAIN_CODE} => #{RULE_NAME} 's event is #{EVENT_STATUS}. The condition is #{RESOURCE_NAME} 's #{DIMENSIONS} #{METRIC} #{OPERATOR} #{CRITERIA}. The current value is #{VALUE}\"\n}",
              "type": "OUT_GOING",
              "updateTime": 1682667085590,
              "url": "https://url"
            }
        }

        pared_data = self.monitoring.Event.parse({'options' : {}, 'data' : cloudinsight_param.get('data')})
        print_json(pared_data)
        print()
        pared_data = self.monitoring.Event.parse({'options' : {}, 'data' : integration_param.get("data")})
        print_json(pared_data)
        print()
