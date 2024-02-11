import logging
import requests
import time
import hashlib
import hmac
import base64
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger("cloudforet")


class WebhookConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_key = kwargs['secret_data'].get('ncloud_access_key_id')
        self.secret_key = kwargs['secret_data'].get('ncloud_secret_key')
        self.page_num = kwargs['page_data'].get('page_num')
        self.page_size = kwargs['page_data'].get('page_size')
        self.prod_key = kwargs['prod_key'].get('prod_key')
        self.base_url = "https://cw.apigw.ntruss.com"

    # def set_connection(self, secret_data):
    #     configuration_server = ncloud_server.Configuration()
    #     configuration_server.access_key = secret_data['ncloud_access_key_id']
    #     configuration_server.secret_key = secret_data['ncloud_secret_key']
    #     self.server_client = ncloud_server.V2Api(ncloud_server.ApiClient(configuration_server))

    def make_signature(self, method, uri):
        timestamp = str(int(time.time() * 1000))
        message = f"{method} {uri}\n{timestamp}\n{self.access_key}"
        signature = base64.b64encode(
            hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        return signature, timestamp

    def call_api(self, method, uri, payload=None):
        signature, timestamp = self.make_signature(method, uri)
        headers = {
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature
        }
        full_url = self.base_url + uri
        if method.upper() == 'POST':
            response = requests.post(full_url, headers=headers, json=payload)
        else:
            response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error(f"API call failed with status code {response.status_code}: {response.text}")
            return None

    def list_metrics_group(self):
        rule_group_list = []
        payload = {
            "prodKey": self.prod_key,
            "pageSize": self.page_size,
            "pageNum": self.page_num,
            "search": ""
        }
        method = "POST"
        uri = "/cw_fea/real/cw/api/rule/group/ruleGrp/query"
        try:
            response = self.call_api(method, uri, payload)  # 수정된 call_api 메소드 호출 시 페이로드 전달
            for group in response['ruleGroups']:
                rule_group_list.append(group)
        except Exception as e:
            _LOGGER.error(f"Exception when calling Cloud Insight API: {e}")

        return rule_group_list
