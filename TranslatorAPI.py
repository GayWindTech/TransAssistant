import random

import urllib
from TranslatorConfig import *
import requests
import time
import uuid
import hashlib
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models


from urllib3 import disable_warnings
disable_warnings()


def truncate(input):
    if input is None:
        return None
    size = len(input)
    return input if size <= 20 else input[0:10] + str(size) + input[size - 10: size]


YOUDAO_ERRORCODE_DICT = {
    101: '缺少必填的参数',
    102: '不支持的语言类型',
    103: '翻译文本过长',
    104: '不支持的API类型',
    105: '不支持的签名类型',
    106: '不支持的响应类型',
    107: '不支持的传输加密类型',
    108: '应用 ID 无效',
    109: 'batchLog格式不正确',
    110: '无相关服务的有效实例',
    111: '开发者账号无效',
    112: '请求服务无效',
    113: '查询字段不能为空',
    114: '不支持的图片传输方式',
    116: 'strict 字段取值无效，请参考文档填写正确参数值',
    201: '解密失败，可能为DES,BASE64,URLDecode的错误',
    202: '签名检验失败，请检查应用ID和应用密钥的正确性',
    203: 'IP地址不在可访问IP列表',
    205: '请求的接口与应用的平台类型不一致',
    206: '因为时间戳无效导致签名校验失败',
    207: '重放请求',
    301: '辞典查询失败',
    302: '翻译查询失败',
    303: '服务端的其它异常',
    304: '会话闲置太久超时',
    401: '账户已经欠费，请进行账户充值',
    402: 'offlinesdk 不可用',
    411: '访问频率受限，请稍后访问',
    412: '长请求过于频繁，请稍后访问'
}

def YoudaoTranslator(QueryText: str) -> str:
    YOUDAO_URL = "https://openapi.youdao.com/api"
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = YOUDAO_KEY + truncate(QueryText) + salt + curtime + YOUDAO_SECRET
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode("utf-8"))
    sign = hash_algorithm.hexdigest()
    _data = {
        "from": "auto",
        "to": "zh-CHS",
        "signType":  "v3",
        "curtime": curtime,
        "appKey": YOUDAO_KEY,
        "q": QueryText,
        "salt": salt,
        "sign": sign,
        "vocabId": ""
    }
    _headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(YOUDAO_URL, data=_data, headers=_headers, verify=False, timeout=5)
        return_dict = json.loads(response.content.decode("utf-8"))
        errorCode = int(return_dict['errorCode'])
        if(errorCode!=0):
            return YOUDAO_ERRORCODE_DICT[errorCode]    
        return return_dict["translation"][0]
    except Exception as err:
        return str(err)


def CaiYunTranslator(QueryText: str) -> str:
    url = "https://api.interpreter.caiyunai.com/v1/translator"
    QueryText = [QueryText]
    payload = {
        "source": QueryText,
        "trans_type": "auto2zh",
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + CAIYUN_TOKEN,
    }
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    except Exception as err:
        return str(err)
    return_dict = json.loads(response.text)
    try:
        return return_dict["target"][0]
    except KeyError:
        return return_dict['message']


def BaiduTranslator(QueryText:str) -> str:
    BAIDU_URL = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = BAIDU_APPID + QueryText + str(salt) + BAIDU_SECRETKEY
    sign = hashlib.md5(sign.encode()).hexdigest()
    request_url = BAIDU_URL + '?appid=' + BAIDU_APPID + '&q=' + urllib.parse.quote(QueryText) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    response = requests.get(request_url, verify=False)
    return_dict = json.loads(response.content.decode('utf-8'))
    try:
        return return_dict['error_msg']
    except KeyError:
        return return_dict['trans_result'][0]['dst']


def TencentTranslator(QueryText:str) -> str:
    try:
        cred = credential.Credential(TENCENT_SECERTID, TENCENT_SECERTKEY)
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
