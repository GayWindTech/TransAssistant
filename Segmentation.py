import MeCab
from sudachipy import tokenizer,dictionary


_MeCab = MeCab.Tagger("-Owakati")
_sudachi = dictionary.Dictionary(dict="full").create()

def splitWords(s,m):
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

# print(splitWords('DIR EN GREYのライブ行きたい','sudachi'))