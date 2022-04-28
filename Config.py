from yaml import CLoader as CLoader, CDumper as CDumper, load as yaml_load, dump as yaml_dump
import sys, os

NOPROXIES = {
    "http": "",
    "https": "",
}

isPacked = (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'))
isInit = True

configPath = f'{os.path.dirname(sys.executable)}/TranslatorConfig.yaml' if isPacked else f'{os.path.dirname(os.path.abspath(__file__))}/TranslatorConfig.yaml'

def writeConfig(data:dict) -> None:
    with open(configPath,mode='w',encoding='utf-8') as f:
        yaml_dump(data,f,CDumper)

def readConfig() -> dict:
    with open(configPath,encoding='utf-8') as f:
        return yaml_load(f,CLoader)

def initConfig() -> None:
    emptyData = {'YOUDAO_KEY': '', 'YOUDAO_SECRET': '', 'CAIYUN_TOKEN': '', 'BAIDU_APPID': '', 'BAIDU_SECRETKEY': '', 'TENCENT_SECERTID': '', 'TENCENT_SECERTKEY': '', 'XIAONIU_KEY':'', 'ALIYUN_KEY':'', 'ALIYUN_SECRET':'', 'SELECTED_TRANSLATORS':[], 'Hotkey_OCR':'Ctrl + Space', 'OCR_APPID':'c788b7aa', 'OCR_SECRET': 'ODFmODQwZWJmZDhlNTIzOTljNGI3OTcy', 'OCR_KEY': '7ec53833f14724cffb810c14e72eef0d'}
    writeConfig(emptyData)

if(not os.path.exists(configPath)):
    isInit = False
    print('Config file not found, creating a new one...')
    initConfig()