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

#http://xf.aka.today/v3/user_info.php?open_id=11111111111111111111111111111111

def getOCRResult(img) -> str:
    def cv2ImgToBytes(img):
        # 如果直接tobytes写入文件会导致无法打开，需要编码成一种图片文件格式(jpg或png)，再tobytes
        # 这里得到的bytes 和 with open("","rb") as f: bytes=f.read()的bytes可能不一样，如果用这里得到的bytes保存过一次，下次就f.read()和cv2ImgToBytes(img)会一样
        return cv2.imencode('.jpg', img)[1].tobytes()


    '''
    appid、apiSecret、apiKey请到讯飞开放平台控制台获取并填写到此demo中；
    图像数据，base64编码后大小不得超过4M
    '''
    # 请到控制台获取以下信息，并填写
    APPId = "c788b7aa"
    APISecret = "ODFmODQwZWJmZDhlNTIzOTljNGI3OTcy"
    APIKey = "7ec53833f14724cffb810c14e72eef0d"
    # 图片位置
    # with open("test/maxresdefault.jpg", "rb") as f:
    #     imageBytes = f.read()
    imageBytes = cv2ImgToBytes(img)

    class AssembleHeaderException(Exception):
        def __init__(self, msg):
            self.message = msg


    class Url:
        def __init__(self, host, path, schema):
            self.host = host
            self.path = path
            self.schema = schema


    # calculate sha256 and encode to base64
    def sha256base64(data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        return base64.b64encode(sha256.digest()).decode(encoding='utf-8')


    def parse_url(requset_url):
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
    def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
        u = parse_url(requset_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # print(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(
            host, date, method, path)
        # print(signature_origin)
        signature_sha = hmac.new(api_secret.encode(
            'utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(
            authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # print(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return f'{requset_url}?{urlencode(values)}'


    url = 'https://api.xf-yun.com/v1/private/s00b65163'

    body = {
        "header": {
            "app_id": APPId,
            "status": 3,
        },
        "parameter": {
            "s00b65163": {
                "category": "mix0",
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "s00b65163_data_1": {
                "encoding": "png",
                "image": str(base64.b64encode(imageBytes), 'UTF-8'),
                "status": 3
            }
        }
    }


    def formatJson(JsonRawText):
        JsonRawDict = json.loads(JsonRawText)
        try:
            for eachPages in JsonRawDict['pages']:
                for eachLines in eachPages['lines']:
                    lineWordsStr = str()
                    for eachWords in eachLines['words']:
                        lineWordsStr += eachWords['content']
                        # print(repr(eachWords['content']))
                    return(lineWordsStr)
        except KeyError:
            return '无法获取有效内容OvO'


    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    try:
        response = requests.post(request_url, data=json.dumps(body), headers=headers,verify=False)
    except Exception as err:
        return str(err)
    tempResult = json.loads(response.content.decode())
    finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
    finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()

    return formatJson(finalResult)
