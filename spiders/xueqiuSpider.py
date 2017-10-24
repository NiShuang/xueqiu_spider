import requests
import json
import time
import re
from config.api import *


class XueqiuSpider():

    def __init__(self):
        pass

    def getPosts(self, code, proxy):
        # s = requests.Session()
        proxies = {
            'http': '',
            'https': proxy
        }
        # header = {
        #     'Host': 'xueqiu.com',
        #     'Pragma': 'no-cache',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        #     'X-Requested-With': 'XMLHttpRequest',
        #     'Connection': 'keep-alive',
        #     'Cache-Control': 'no-cache',
        #     'Accept-Language': 'zh-CN,zh;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept': 'application/json, text/javascript, */*; q=0.01',
        #     'Upgrade-Insecure-Requests': '1'
        # }
        # r = s.get('https://xueqiu.com', headers=header, proxies=proxies, verify=False)
        # jar = r.cookies
        # cookie_dict =  requests.utils.dict_from_cookiejar(jar)
        # print cookie_dict
        # cookie = ''
        # for index in cookie_dict:
        #     cookie += index + '=' + cookie_dict[index] + '; '
        # print cookie
        result = []
        para = {
            'count': 10,
            'sort': 'time',
            'source': 'all',
            'comment': 0,
            'symbol': code,
            'hl': 0
        }
        header = {
            'Host': 'xueqiu.com',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 's=ec11tqq28f; device_id=2ec5071cc96b700dd2efb5ef65a66286; xq_a_token=c1040132b0c18a2606d22253088b2ced49e947cd; xqat=c1040132b0c18a2606d22253088b2ced49e947cd; xq_r_token=cad321de6928d86096f70cae0da65a6b2e672c7e; xq_is_login=1; u=9886119632; xq_token_expire=Thu%20Nov%2009%202017%2017%3A11%3A14%20GMT%2B0800%20(CST); bid=f5f1c4b1605d770da509c5687ef67837_j8sj74i2; aliyungf_tc=AQAAAPOlZ33sPwAAVVGi02fCyV+Zgt4v',
            # 'Cookie': cookie,
            'Referer': baseUrl + code,
            'Upgrade-Insecure-Requests': '1'
        }
        para['page'] = 1
        para['_'] = str(int(time.time())) + '000'
        try:
            req = requests.get(postApi, params=para, headers=header, proxies=proxies)
            # print req.text
        except:
            time.sleep(120)
            req = requests.get(postApi, params=para, headers=header, proxies=proxies)
            # print req.text
        jsonData = json.loads(req.text)
        result.extend(jsonData['list'])
        maxPage = jsonData['maxPage']
        count = 0
        for page in range(2, maxPage + 1):
            para['page'] = page
            para['_'] = str(int(time.time())) + '000'
            try:
                req = requests.get(postApi, params=para, headers=header, proxies=proxies)
            except:
                time.sleep(600)
                req = requests.get(postApi, params=para, headers=header, proxies=proxies)
            jsonData = json.loads(req.text)
            try:
                result.extend(jsonData['list'])
            except:
                time.sleep(300)
                req = requests.get(postApi, params=para, headers=header, proxies=proxies)
                jsonData = json.loads(req.text)
                result.extend(jsonData['list'])
            count += 1
            if count % 10 == 0:
                time.sleep(5)
            time.sleep(0.3)
        return result


    def getReply(self, postID):
        result = []
        para = {
            'reply': 'true',
            'filtered': 'true',
            'callback': '',
            'id': postID
        }
        header = {
            'Host': 'xueqiu.com',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Cookie': 's=ec11tqq28f; device_id=2ec5071cc96b700dd2efb5ef65a66286; xq_a_token=c1040132b0c18a2606d22253088b2ced49e947cd; xqat=c1040132b0c18a2606d22253088b2ced49e947cd; xq_r_token=cad321de6928d86096f70cae0da65a6b2e672c7e; xq_is_login=1; u=9886119632; xq_token_expire=Thu%20Nov%2009%202017%2017%3A11%3A14%20GMT%2B0800%20(CST); bid=f5f1c4b1605d770da509c5687ef67837_j8sj74i2; aliyungf_tc=AQAAAPOlZ33sPwAAVVGi02fCyV+Zgt4v',
            'Content-Length': '0',
            'Origin': 'https://xueqiu.com',
            # 'Referer': baseUrl + code
        }
        formData = {
            'asc': 'false'
        }
        req = requests.post(replyApi, params=para, data=formData, headers=header, verify=False)
        print req.text
        jsonData = json.loads(req.text)
        result.extend(jsonData['comments'])
        maxPage = jsonData['maxPage']
        count = 0
        for page in range(2, maxPage + 1):
            formData['page'] = page
            req = requests.post(replyApi, params=para, data=formData, headers=header, verify=False)
            print req.text
            jsonData = json.loads(req.text)
            result.extend(jsonData['comments'])
            count += 1
            time.sleep(0.3)
        return result


    def getUserInfo(self, userID):
        header = {
            'Host': 'xueqiu.com',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cookie': 'aliyungf_tc=AQAAAOQVvUpu9QsAVVGi0yYC+i+XlSXx; s=ec11tqq28f; xq_a_token=e3cae829e5836e234be00887406080b41c2cb69a; xq_r_token=319673aba44e00bd0fed3702652be32b2349860e; u=831507954742513; device_id=2ec5071cc96b700dd2efb5ef65a66286; Hm_lvt_1db88642e346389874251b5a1eded6e3=1507954742; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1507985857; __utmt=1; __utma=1.491447245.1507954745.1507980513.1507985857.6; __utmb=1.1.10.1507985857; __utmc=1; __utmz=1.1507954745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'Content-Length': '0',
            'Origin': 'https://xueqiu.com',
            'Referer': 'https://xueqiu.com'
        }
        req = requests.get('https://xueqiu.com/' + str(userID),  headers=header, verify=False, allow_redirects=False)
        page = req.text
        pattern = re.compile("</script><script>SNB.profileUser = (.*?)</script><noscript>", re.S)
        items = re.findall(pattern, page)
        data = items[0]
        print data
        try:
            data = json.loads(data)
        except:
            return None
        stock_list = self.getStocksByUser(userID)
        for stock in stock_list:
            stock.pop('comment')
            stock.pop('sellPrice')
            stock.pop('buyPrice')
            stock.pop('portfolioIds')
            stock.pop('isNotice')
            stock.pop('targetPercent')
        data['stock_list'] = stock_list
        return data

    def getStocksByUser(self, userID):
        para = {
            'size': 1000,
            'pid': -1,
            'tuid': userID,
            'uid': userID,
            'category': 2,
            'type': 1,
            '_': str(int(time.time())) + '000'
        }
        header = {
            'Host': 'xueqiu.com',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': 'aliyungf_tc=AQAAAOQVvUpu9QsAVVGi0yYC+i+XlSXx; s=ec11tqq28f; xq_a_token=e3cae829e5836e234be00887406080b41c2cb69a; xq_r_token=319673aba44e00bd0fed3702652be32b2349860e; u=831507954742513; device_id=2ec5071cc96b700dd2efb5ef65a66286; Hm_lvt_1db88642e346389874251b5a1eded6e3=1507954742; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1507985857; __utmt=1; __utma=1.491447245.1507954745.1507980513.1507985857.6; __utmb=1.1.10.1507985857; __utmc=1; __utmz=1.1507954745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'Content-Length': '0',
            'Origin': 'https://xueqiu.com',
            'Referer': 'https://xueqiu.com/' + str(userID)
        }
        try:
            req = requests.get(stockApi, params=para, headers=header, verify=False)
        except:
            time.sleep(180)
            req = requests.get(stockApi, params=para, headers=header, verify=False)
        print req.text
        result = json.loads(req.text)
        return result['stocks']


    def get_stocks_trade(self, stock_list):
        result = {}
        header = {
            'Host': 'xueqiu.com',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': 'aliyungf_tc=AQAAAOQVvUpu9QsAVVGi0yYC+i+XlSXx; s=ec11tqq28f; xq_a_token=e3cae829e5836e234be00887406080b41c2cb69a; xq_r_token=319673aba44e00bd0fed3702652be32b2349860e; u=831507954742513; device_id=2ec5071cc96b700dd2efb5ef65a66286; Hm_lvt_1db88642e346389874251b5a1eded6e3=1507954742; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1507985857; __utmt=1; __utma=1.491447245.1507954745.1507980513.1507985857.6; __utmb=1.1.10.1507985857; __utmc=1; __utmz=1.1507954745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'Content-Length': '0',
            'Origin': 'https://xueqiu.com'
        }
        stocks_code = ''
        index = 0
        for stock in stock_list:
            stocks_code += stock['code'] + ','
            index += 1
            if index % 50 == 0 or index == len(stock_list):
                para = {
                    'code': stocks_code,
                    '_': str(int(time.time())) + '000'
                }
                try:
                    req = requests.get(stockInfoUrl, params=para, headers=header)
                except:
                    time.sleep(180)
                    req = requests.get(stockInfoUrl, params=para, headers=header)
                print req.text
                result = dict(result, **(json.loads(req.text)))
                stocks_code = ''
        for stock in stock_list:
            try:
                stock['price'] = result[stock['code']]['current']
                stock['reduced_code'] = result[stock['code']]['code']
            except:
                pass
        return stock_list
if __name__ == '__main__':
    s = XueqiuSpider()
    s.getUserInfo(1121939593)
    # s.getPosts('SH600004')
    # s.getReply('SH600004', '93713258')
    # s.getStocksByUser('1121939593')