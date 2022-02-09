import random

import urllib
from urllib import response
from TranslatorConfig import *
import requests
import time
import uuid
import hashlib
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.tmt.v20180321 import tmt_client, models


from urllib3 import disable_warnings
disable_warnings()


def truncate(input):
    if input is None:
        return None
    size = len(input)
    return input if size <= 20 else input[0:10] + str(size) + input[size - 10: size]

def YoudaoTranslator(QueryText: str, key=YOUDAO_KEY, secret=YOUDAO_SECRET) -> str:
    YOUDAO_URL = "https://openapi.youdao.com/api"
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = key + truncate(QueryText) + salt + curtime + secret
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode("utf-8"))
    sign = hash_algorithm.hexdigest()
    _data = {
        "from": "auto",
        "to": "zh-CHS",
        "signType":  "v3",
        "curtime": curtime,
        "appKey": key,
        "q": QueryText,
        "salt": salt,
        "sign": sign,
        "vocabId": ""
    }
    _headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(YOUDAO_URL, data=_data, headers=_headers, verify=False, proxies=None)
    return json.loads(response.content.decode("utf-8"))["translation"][0]


def CaiYunTranslator(QueryText: str, CaiYun_Token=CAIYUN_TOKEN) -> str:
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    QueryText = [QueryText]
    payload = {
        "source": QueryText,
        "trans_type": "auto2zh",
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + CaiYun_Token,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, proxies=None)
    return json.loads(response.text)["target"][0]


def BaiduTranslator(QueryText:str,appid=BAIDU_APPID, scretKey=BAIDU_SECRETKEY) -> str:
    BAIDU_URL = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + QueryText + str(salt) + scretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    request_url = BAIDU_URL + '?appid=' + appid + '&q=' + urllib.parse.quote(QueryText) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    response = requests.get(request_url, verify=False, proxies=None)
    return json.loads(response.content.decode('utf-8'))['trans_result'][0]['dst']


def TencentTranslator(QueryText:str, SecretId=TENCENT_SECERTID, SecretKey=TENCENT_SECERTKEY) -> str:
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)
        req = models.TextTranslateRequest()
        params = {
            "SourceText": QueryText,
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
        return str(err)
