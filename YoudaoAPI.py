# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
from importlib import reload
import time
import json
from urllib3 import disable_warnings

disable_warnings()


reload(sys)

YOUDAO_URL = "https://openapi.youdao.com/api"
APP_KEY = ""
APP_SECRET = ""


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode("utf-8"))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]


def do_request(data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(YOUDAO_URL, data=data, headers=headers, verify=False)


def YoudaoTranslator(q: str) -> str:

    data = {}
    data["from"] = "auto"
    data["to"] = "zh-CHS"
    data["signType"] = "v3"
    curtime = str(int(time.time()))
    data["curtime"] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data["appKey"] = APP_KEY
    data["q"] = q
    data["salt"] = salt
    data["sign"] = sign
    data["vocabId"] = ""

    response = do_request(data)
    result = json.loads(response.content.decode("utf-8"))["translation"][0]
    return result
