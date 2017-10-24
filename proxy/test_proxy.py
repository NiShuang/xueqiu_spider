# -*- coding: UTF-8 -*-
import requests

def test_proxy(ip, port):
    proxies = {
        'https': 'http://' + ip + ':' + port
    }
    try:
        requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
        # print req.text
        return True
    except:
        return False
