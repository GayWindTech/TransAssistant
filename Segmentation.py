from fugashi import Tagger # from MeCab import Tagger
import csv
from sudachipy import tokenizer,dictionary
import requests
import json
from urllib3 import disable_warnings
from os import path
from sys import executable,argv
disable_warnings()
isPacked = executable == argv[0]

def _kuromoji(s: str) -> list:
    output = list()
    url = "https://www.atilika.org/kuromoji/rest/tokenizer/tokenize"
    datas = {"text": s, "mode": 0}
    req = requests.post(url, data=datas, verify=False, proxies=None)
    # var_dump(json.loads(req.content.decode('utf-8'))['tokens'])
    for each in json.loads(req.content.decode("utf-8"))["tokens"]:
        output.append(each["surface"])
    return output


_MeCab = Tagger("-Owakati")
if(isPacked):
    sudachi_dict_path = path.abspath(path.join(path.dirname(__file__), r'sudachidict_full\resources\system.dic'))
    sudachi_config_path = path.abspath(path.join(path.dirname(__file__), r'sudachipy\resources\sudachi.json'))
    _sudachi = dictionary.Dictionary(dict=sudachi_dict_path,config_path=sudachi_config_path).create()
else:
    _sudachi = dictionary.Dictionary(dict="full").create()

def splitWords(s, m):
    output = str()
    if(m == "MeCab"):
        temp = _MeCab.parse(s).split()
        for each in temp:
            if(each != " " and each != None):
                output += each + " | "
        return output
    elif(m == "sudachi"):
        mode = tokenizer.Tokenizer.SplitMode.B
        temp = [m.surface() for m in _sudachi.tokenize(s, mode)]
        for each in temp:
            if(each != " " and each != None):
                output += each + " | "
        return output
    elif(m == "kuromoji"):
        temp = _kuromoji(s)
        for each in temp:
            if each != " " and each != None:
                output += each + " | "
        return output


# print(splitWords("DIR EN GREYのライブ行きたい", "sudachi"))
