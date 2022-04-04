from fugashi import Tagger # from MeCab import Tagger
import csv
from sudachipy import tokenizer,dictionary
import requests
import json
from urllib3 import disable_warnings
from os import path
disable_warnings()
from Config import isPacked

def _kuromoji(s: str) -> list:
    url = "https://www.atilika.org/kuromoji/rest/tokenizer/tokenize"
    datas = {"text": s, "mode": 0}
    req = requests.post(url, data=datas, verify=False, proxies=None)
    # var_dump(json.loads(req.content.decode('utf-8'))['tokens'])
    return (each["surface"] for each in json.loads(req.content.decode("utf-8"))["tokens"] )


try:
    import unidic
    unidic_dicdir = path.abspath(path.join(path.dirname(__file__), r'unidic\dicdir')) if isPacked else unidic.DICDIR
    print('SudachiDict: Normal')
except ModuleNotFoundError:
    import unidic_lite
    unidic_dicdir = path.abspath(path.join(path.dirname(__file__), r'unidic_lite\dicdir')) if isPacked else unidic_lite.DICDIR
    print(unidic_dicdir)
    print('SudachiDict: Lite')
print(unidic_dicdir)
_MeCab = Tagger(f'-Owakati -d "{unidic_dicdir}"')

sudachi_config_path = path.abspath(path.join(path.dirname(__file__), r'sudachipy\resources\sudachi.json')) if isPacked else None
try:
    _sudachi = dictionary.Dictionary(dict="full",config_path=sudachi_config_path).create()
    print('SudachiDict: Full')
except ModuleNotFoundError:
    try:
        _sudachi = dictionary.Dictionary(dict="core",config_path=sudachi_config_path).create()
        print('SudachiDict: Core')
    except ModuleNotFoundError:
        _sudachi = dictionary.Dictionary(dict="small",config_path=sudachi_config_path).create()
        print('SudachiDict: Small')

def splitWords(s, m):
    output = str()
    if (m == "MeCab"):
        temp = _MeCab.parse(s).split()
        for each in temp:
            if (each not in (" ", None)):
                output += f'{each} | '
        return output
    elif (m == "sudachi"):
        mode = tokenizer.Tokenizer.SplitMode.B
        temp = [m.surface() for m in _sudachi.tokenize(s, mode)]
        for each in temp:
            if (each not in (" ", None)):
                output += f'{each} | '
        return output
    elif (m == "kuromoji"):
        temp = _kuromoji(s)
        for each in temp:
            if (each not in (" ", None)):
                output += f'{each} | '
        return output


# print(splitWords("DIR EN GREYのライブ行きたい", "sudachi"))
