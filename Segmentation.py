# from MeCab import Tagger
# from sudachipy import tokenizer,dictionary
import requests
import json
from urllib3 import disable_warnings

disable_warnings()


def _kuromoji(s: str) -> list:
    output = list()
    url = "https://www.atilika.org/kuromoji/rest/tokenizer/tokenize"
    datas = {"text": s, "mode": 0}
    req = requests.post(url, data=datas, verify=False)
    # var_dump(json.loads(req.content.decode('utf-8'))['tokens'])
    for each in json.loads(req.content.decode("utf-8"))["tokens"]:
        output.append(each["surface"])
    return output


# _MeCab = Tagger("-Owakati")
# _sudachi = dictionary.Dictionary(dict="full").create()


def splitWords(s, m):
    output = str()
    # if(m == "MeCab"):
    #     temp = _MeCab.parse(s).split()
    #     for each in temp:
    #         if(each != " " and each != None):
    #             output += each + " | "
    #     return output
    # elif(m == "sudachi"):
    #     mode = tokenizer.Tokenizer.SplitMode.B
    #     temp = [m.surface() for m in _sudachi.tokenize(s, mode)]
    #     for each in temp:
    #         if(each != " " and each != None):
    #             output += each + " | "
    #     return output
    temp = _kuromoji(s)
    for each in temp:
        if each != " " and each != None:
            output += each + " | "
    return output


# print(splitWords("DIR EN GREYのライブ行きたい", "sudachi"))
