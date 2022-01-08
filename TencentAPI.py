import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.tmt.v20180321 import tmt_client, models


def TencentTranslator(q):
    try:
        cred = credential.Credential(
            "", ""
        )
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)

        req = models.TextTranslateRequest()
        params = {
            "SourceText": q,
            "Source": "auto",
            "Target": "zh",
            "ProjectId": 0,
            "UntranslatedText": "",
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextTranslate(req)
        result = json.loads(resp.to_json_string())
        return result['TargetText']

    except TencentCloudSDKException as err:
        # print(err)
        return str(err)
