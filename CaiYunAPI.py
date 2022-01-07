def CaiYunTranslator(source):

    import requests
    import json
    
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    
    #WARNING, this token is a test token for new developers, and it should be replaced by your token
    token = ""
    
    source = [source]
    
    payload = {
            "source" : source, 
            "trans_type" : 'auto2zh',
            "request_id" : "demo",
            "detect": True,
            }
    
    headers = {
            'content-type': "application/json",
            'x-authorization': "token " + token,
    }
    
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)['target'][0]
