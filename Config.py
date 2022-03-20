from yaml import CLoader as CLoader, CDumper as CDumper, load as yaml_load, dump as yaml_dump
import sys, os

isPacked = getattr(sys, 'frozen', False)

configPath = f'{os.path.dirname(sys.executable)}/TranslatorConfig.yaml' if isPacked else f'{os.path.dirname(os.path.abspath(__file__))}/TranslatorConfig.yaml'

def initConfig() -> None:
    emptyData = {'YOUDAO_KEY': '', 'YOUDAO_SECRET': '', 'CAIYUN_TOKEN': '', 'BAIDU_APPID': '', 'BAIDU_SECRETKEY': '', 'TENCENT_SECERTID': '', 'TENCENT_SECERTKEY': ''}
    with open(configPath,mode='w',encoding='utf-8') as f:
        yaml_dump(emptyData,f,CDumper)

if(not os.path.exists(configPath)):
    initConfig()

def readConfig() -> dict:
    with open(configPath,encoding='utf-8') as f:
        return yaml_load(f,CLoader)
