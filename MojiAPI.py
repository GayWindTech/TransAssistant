# coding=utf-8
import itertools
import requests
import json
from Config import NOPROXIES
# from var_dump import var_dump
from urllib3 import disable_warnings

disable_warnings()

def searchWord(word: str) -> list:
    try:
        APIURL = "https://api.mojidict.com/parse/functions/search_v3"
        hd = {
            "content-type": "text/plain",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        JsonDict = {
            "searchText": word,
            "langEnv": "zh-CN_ja",
            "needWords": True,
            "_ClientVersion": "js2.12.0",
            "_SessionToken": "r:ac5e644394986753026f2e6fb76a1cc5",
            "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        }
        req = requests.post(APIURL, json=JsonDict, headers=hd, verify=False,proxies=NOPROXIES)
        resultTemp = json.loads(req.content.decode("utf-8"))["result"]["searchResults"]
        return [(eachWordDict['title'].replace('◎','⓪'),eachWordDict['tarId']) for eachWordDict in resultTemp if 'http' not in eachWordDict['tarId']]
    except KeyError:
        return [('发生了错误','0')]
    except Exception as err:
        return [(f'未知错误,：{str(err)}', '0')]

def fetchWord(id: str) -> tuple|str:
    try:
        APIURL = "https://api.mojidict.com/parse/functions/fetchWord_v2"
        hd = {
            "content-type": "text/plain",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        JsonDict = {
            "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
            "_ClientVersion": "js2.12.0",
            "_InstallationId": "f8bd75b5-9499-e4ec-634b-1a5544681285",
            "wordId": id,
        }
        req = requests.post(APIURL, json=JsonDict, headers=hd, verify=False, proxies=NOPROXIES)
        return parseFetchResult(json.loads(req.content.decode("utf-8"))["result"])
    except Exception as e:
        return f'发生了错误，请向开发者报告：{str(e)} File "MojiAPI.py", in fetchWord'

def parseFetchResult(resultTemp: dict) -> tuple|str:
    try:
        excerpt = resultTemp['word']['excerpt']
        spell = resultTemp['word']['spell']
        accent = resultTemp['word']['accent']
        pron = resultTemp['word']['pron']
        detailDict = [[eachDetail['objectId'] for eachDetail in resultTemp['details']],{eachDetail['objectId']: [eachDetail['title'],[],{}] for eachDetail in resultTemp['details']}]
        for eachSubDetails in resultTemp['subdetails']:
            if(eachSubDetails['detailsId'] in detailDict[1]):
                detailDict[1][eachSubDetails['detailsId']][1].append(eachSubDetails['objectId']) # type: ignore
                detailDict[1][eachSubDetails['detailsId']][2][eachSubDetails['objectId']] = [eachSubDetails['title'],[]] # type: ignore
        if ('examples' in resultTemp):
            for eachExample, eachDetailId in itertools.product(resultTemp['examples'], detailDict[0]):
                if(eachExample['subdetailsId'] in detailDict[1][eachDetailId][1]): # type: ignore
                    detailDict[1][eachDetailId][2][eachExample['subdetailsId']][1].append((eachExample['title'],eachExample['trans'])) # type: ignore
        return ((spell,excerpt,pron,accent.replace('◎','⓪')),detailDict)
    except Exception as err:
        return f'发生了错误，请向开发者报告：{str(err)} File "MojiAPI.py", in parseFetchResult'
