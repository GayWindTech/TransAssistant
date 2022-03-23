# Translation Assistant

> 基于OCR的日语翻译辅助工具

[![Release](https://img.shields.io/github/v/release/GayWindTech/TransAssistant)](https://github.com/GayWindTech/TransAssistant/releases)
[![Build](https://github.com/GayWindTech/TransAssistant/workflows/Package%20Application%20with%20Pyinstaller/badge.svg?branch=main)](https://github.com/GayWindTech/TransAssistant/blob/main/.github/workflows/pyInstaller.yml)

## Installation
### 可执行文件
从[Release](https://github.com/GayWindTech/TransAssistant/releases)中下载最新版本并解压，运行`GUI.exe`即可
### 源码运行
如果你是开发者，或者对python有所了解，也可以使用源码运行
1. 将项目克隆到本地
2. 在工作目录下执行：
    ``` 
    $ pip install -r requirements.txt
    $ python -m unidic download
    $ python GUI.py
    ```

## Usage
### TranslatorConfig.yaml
使用前首先要在工作目录下的 `TranslatorConfig.yaml` 文件填写各翻译API的密钥
```
# 百度翻译
BAIDU_APPID: ''
BAIDU_SECRETKEY: ''

# 彩云小译
CAIYUN_TOKEN: ''

# 腾讯翻译
TENCENT_SECERTID: ''
TENCENT_SECERTKEY: ''

# 有道翻译
YOUDAO_KEY: ''
YOUDAO_SECRET: ''
```
#### 申请方法：
1. 百度翻译：可参考 https://hcfy.app/docs/services/baidu-api
2. 彩云小译：可参考 https://hcfy.app/docs/services/caiyun-api
3. 腾讯翻译：可参考 https://hcfy.app/docs/services/qq-api
4. 有道翻译：可参考 https://hcfy.app/docs/services/youdao-api

注：如果使用源码运行，找不到`TranslatorConfig.yaml`，可以运行一次主程序自动创建

## License
[License](https://github.com/GayWindTech/TransAssistant/blob/main/LICENSE)
