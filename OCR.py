# from var_dump import var_dump
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
import cv2
from urllib3 import disable_warnings
disable_warnings()

from Config import readConfig
configs = readConfig()

def reloadOCRConfig():
    global configs
    configs = readConfig()


def cv2ImgToBytes(img):
    # 如果直接tobytes写入文件会导致无法打开，需要编码成一种图片文件格式(jpg或png)，再tobytes
    # 这里得到的bytes 和 with open("","rb") as f: bytes=f.read()的bytes可能不一样，如果用这里得到的bytes保存过一次，下次就f.read()和cv2ImgToBytes(img)会一样
    return cv2.imencode('.jpg', img)[1].tobytes()


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema


# calculate sha256 and encode to base64
def sha256base64(data) -> str:
    sha256 = hashlib.sha256()
    sha256.update(data)
    return base64.b64encode(sha256.digest()).decode(encoding='utf-8')


def parse_url(requset_url: str):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException(f"invalid request url:{requset_url}")
    path = host[edidx:]
    host = host[:edidx]
    return Url(host, path, schema)


# build websocket auth request url
def assemble_ws_auth_url(requset_url: str, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (api_key, "hmac-sha256", "host date request-line", signature_sha)
    
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {"host": host, "date": date, "authorization": authorization}
    return f'{requset_url}?{urlencode(values)}'


def formatJson(JsonRawText: str) -> str:
    JsonRawDict = json.loads(JsonRawText)
    try:
        for eachPages in JsonRawDict['pages']:
            for eachLines in eachPages['lines']:
                lineWordsStr = str()
                for eachWords in eachLines['words']:
                    lineWordsStr += eachWords['content']
                return(lineWordsStr)
    except KeyError:
        return '无法获取有效内容OvO'

def checkSecretAvailable(appId: str, apiSecret: str, apiKey: str) -> bool:
    url = 'https://api.xf-yun.com/v1/private/s00b65163'
    _body = {"header": {"app_id": appId, "status": 3}, "parameter": {"s00b65163": {"category": "mix0", "result": {"encoding": "utf8", "compress": "raw", "format": "json"}}}}
    request_url = assemble_ws_auth_url(url, "POST", apiKey, apiSecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': appId}
    try:
        response = requests.post(request_url, data=json.dumps(_body), headers=headers,verify=False)
        return json.loads(response.content.decode())['header']['code'] == 10009
    except Exception:
        return False

def getOCRResult(img) -> str:
    imageBytes = cv2ImgToBytes(img)
    url = 'https://api.xf-yun.com/v1/private/s00b65163'
    body = {"header": {"app_id": configs['OCR_APPID'], "status": 3}, "parameter": {"s00b65163": {"category": "mix0", "result": {"encoding": "utf8", "compress": "raw", "format": "json"}}}, "payload": {"s00b65163_data_1": {"encoding": "png", "image": str(base64.b64encode(imageBytes), 'UTF-8'), "status": 3}}}
    request_url = assemble_ws_auth_url(url, "POST", configs['OCR_KEY'], configs['OCR_SECRET'])
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': configs['OCR_APPID']}
    try:
        response = requests.post(request_url, data=json.dumps(body), headers=headers,verify=False)
        tempResult = json.loads(response.content.decode())
        finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
        finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    except Exception as err:
        return f'OCR出错：{err}'

    return formatJson(finalResult)

def getOCRSecret() -> tuple:
    url = "aHR0cDovL3hmLmFrYS50b2RheS92My91c2VyX2luZm8ucGhwP29wZW5faWQ9ZmZkNjI2NDM0NDI1NDQ5MDk3YzcxZmUwMGJmYTBmNTU="
    return tuple((eachDict['appId'], eachDict['apiSecret2'], eachDict['apiKey2']) for eachDict in requests.get(base64.b64decode(url)).json()['data']['all_share'] if(eachDict['apiKey2'] and eachDict['apiSecret2']))

def getVaildOCRSecert() -> tuple:
    return tuple(each for each in getOCRSecret() if(checkSecretAvailable(each[0], each[1], each[2])))
