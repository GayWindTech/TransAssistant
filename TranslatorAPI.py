from distutils.log import error
import random

import urllib
from Config import readConfig
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

configs = readConfig()

def truncate(input):
    if input is None:
        return None
    size = len(input)
    return input if size <= 20 else input[:10] + str(size) + input[size - 10: size]

CONFIG_REMIND = "，请检查TranslatorConfig.yaml文件是否准确填写。"
UNDEFINED_ERROR_MESSAGE = "未知错误，请联系开发者"

YOUDAO_ERRORCODE_DICT = {
    101: '缺少必填的参数',
    102: '不支持的语言类型',
    103: '翻译文本过长',
    104: '不支持的API类型',
    105: '不支持的签名类型',
    106: '不支持的响应类型',
    107: '不支持的传输加密类型',
    108: '应用 ID 无效' + CONFIG_REMIND,
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

BAIDU_ERRORCODE_DICT = {
    '52001': '请求超时',
    '52002': '系统错误',
    '52003': '未授权用户' + CONFIG_REMIND,
    '54000': '必填参数为空',
    '54001': '签名错误',
    '54003': '访问频率受限',
    '54004': '账户余额不足',
    '54005': '长query请求频繁',
    '58000': '客户端IP非法',
    '58001': '译文语言方向不支持',
    '58002': '服务当前已关闭',
    '90107': '认证未通过或未生效',
}

TENCENT_ERRORCODE_DICT = {
    'InvalidCredential':'ID无效' + CONFIG_REMIND,
    'FailedOperation.NoFreeAmount':'本月免费额度已用完',
    'FailedOperation.ServiceIsolate': '账号因为欠费停止服务',
    'FailedOperation.UserNotRegistered': '服务未开通',
    'InternalError': '内部错误',
    'InternalError.BackendTimeout': '后台服务超时，请稍后重试',
    'InternalError.ErrorUnknown': '未知错误',
    'InternalError.RequestFailed': '请求失败',
    'InvalidParameter': '参数错误',
    'InvalidParameter.MissingParameter': '参数错误',
    'LimitExceeded': '超过配额限制',
    'LimitExceeded.LimitedAccessFrequency': '超出请求频率',
    'MissingParameter': '缺少参数错误',
    'UnauthorizedOperation.ActionNotFound': '请填写正确的Action字段名称',
    'UnsupportedOperation': '操作不支持',
    'UnsupportedOperation.TextTooLong': '单次请求text超过长度限制',
    'UnsupportedOperation.UnSupportedTargetLanguage': '不支持的目标语言',
    'UnsupportedOperation.UnsupportedLanguage': '不支持的语言',
    'UnsupportedOperation.UnsupportedSourceLanguage': '不支持的源语言',
}

CAIYUN_ERRORCODE_DICT = {
    'Invalid token': 'Token无效' + CONFIG_REMIND
}

def YoudaoTranslator(QueryText: str) -> str:
    YOUDAO_URL = "https://openapi.youdao.com/api"
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = configs['YOUDAO_KEY'] + truncate(QueryText) + salt + curtime + configs['YOUDAO_SECRET']
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode("utf-8"))
    sign = hash_algorithm.hexdigest()
    _data = {
        "from": "auto",
        "to": "zh-CHS",
        "signType":  "v3",
        "curtime": curtime,
        "appKey": configs['YOUDAO_KEY'],
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
            return YOUDAO_ERRORCODE_DICT.get(errorCode, "未知错误:" + return_dict['errorCode'])
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
        "x-authorization": f"token {configs['CAIYUN_TOKEN']}",
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    except Exception as err:
        return str(err)
    return_dict = json.loads(response.content)
    try:
        return return_dict["target"][0]
    except KeyError:
        return CAIYUN_ERRORCODE_DICT.get(return_dict['message'], return_dict['message'])
    except Exception as e:
        return str(e)


def BaiduTranslator(QueryText:str) -> str:
    BAIDU_URL = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = configs['BAIDU_APPID'] + QueryText + str(salt) + configs['BAIDU_SECRETKEY']
    sign = hashlib.md5(sign.encode()).hexdigest()
    request_url = (f'{BAIDU_URL}?appid=' + configs['BAIDU_APPID']+ '&q=' + urllib.parse.quote(QueryText)+ '&from=' + fromLang+ '&to=' + toLang+ '&salt=' + str(salt)+ '&sign=' + sign)


    response = requests.get(request_url, verify=False)
    return_dict = json.loads(response.content.decode('utf-8'))
    try:
        return return_dict['trans_result'][0]['dst']
    except KeyError:
        return BAIDU_ERRORCODE_DICT.get(return_dict['error_code'], "未知错误:" + return_dict['error_code']) + return_dict['error_msg']
    except Exception as e:
        return str(e)


def TencentTranslator(QueryText:str) -> str:
    try:
        cred = credential.Credential(configs['TENCENT_SECERTID'], configs['TENCENT_SECERTKEY'])
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
        return TENCENT_ERRORCODE_DICT.get(err.code, err.code) + err.message
    except Exception as e:
        return str(e)