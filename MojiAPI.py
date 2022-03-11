# coding=utf-8
import requests
import json
from var_dump import var_dump
from urllib3 import disable_warnings

disable_warnings()


def searchWord(word: str) -> list:
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
        "_SessionToken": "r:1e9b36707888bfcfc7c0b6349df75761",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    }
    req = requests.post(APIURL, json=JsonDict, headers=hd, verify=False)
    try:
        resultTemp = json.loads(req.content.decode("utf-8"))["result"]["searchResults"]
        return [(eachWordDict['title'].replace('◎','⓪'),eachWordDict['tarId']) for eachWordDict in resultTemp if 'http' not in eachWordDict['tarId']]
    except KeyError:
        return [('发生了错误','0')]

def fetchWord(id: str) -> dict:
    APIURL = "https://api.mojidict.com/parse/functions/fetchWord_v2"
    hd = {
        "content-type": "text/plain",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }
    JsonDict = {
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        "_ClientVersion": "js2.12.0",
        "_InstallationId": "f8bd75b5-9499-e4ec-634b-1a5544681285",
        "wordId": str(id),
    }
    req = requests.post(APIURL, json=JsonDict, headers=hd, verify=False)
    return parseFetchResult(json.loads(req.content.decode("utf-8"))["result"])

def parseFetchResult(resultTemp: dict) -> tuple:
    try:
        excerpt = resultTemp['word']['excerpt']
        spell = resultTemp['word']['spell']
        accent = resultTemp['word']['accent']
        pron = resultTemp['word']['pron']
        detailDict = [[eachDetail['objectId'] for eachDetail in resultTemp['details']],{eachDetail['objectId']: [eachDetail['title'],[],{}] for eachDetail in resultTemp['details']}]
        for eachSubDetails in resultTemp['subdetails']:
            if(eachSubDetails['detailsId'] in detailDict[1]):
                detailDict[1][eachSubDetails['detailsId']][1].append(eachSubDetails['objectId'])
                detailDict[1][eachSubDetails['detailsId']][2][eachSubDetails['objectId']] = [eachSubDetails['title'],[]]
        if('examples' in resultTemp):
            for eachExample in resultTemp['examples']:
                for eachDetailId in detailDict[0]:
                    if(eachExample['subdetailsId'] in detailDict[1][eachDetailId][1]):
                        detailDict[1][eachDetailId][2][eachExample['subdetailsId']][1].append((eachExample['title'],eachExample['trans']))
        return ((spell,excerpt,pron,accent.replace('◎','⓪')),detailDict)
    except Exception as err:
        return f'发生了错误，请向开发者报告：{str(err)}'
