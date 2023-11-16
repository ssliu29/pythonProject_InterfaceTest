"""
    2.1.1获取测试数据内进行请求时需要的关键字段
    2.1.2进行请求，获取返回结果
"""
import json

import requests
from common.readConfig import ReadConfig

rc = ReadConfig()
URL = rc.get_config("url", "base_url")

class ConfigHttp:
    def __init__(self, dic):
        self.dic = dic

    def run(self):
        # 2.1.1获取测试数据类进行请求时需要的关键字段
        interfaceUrl = URL + self.dic["interfaceUrl"]
        method = self.dic["method"]
        value = self.dic["value"]
        expect = self.dic["expect"]
        print("===>", interfaceUrl, method, value, expect)
        # 2.1.2进行请求，获取返回结果
        if method.lower() == "get":
            res = self.__get()
            return res
        elif method.lower() == "post":
            res = self.__post()
            return res

    def __get(self):
        res = requests.get(url=URL+self.dic["interfaceUrl"],
                           params=eval(self.dic["value"]),
                           headers=eval(self.dic["header"]))
        return res

    def __post1(self):
        res = requests.post(url=URL+self.dic["interfaceUrl"],
                            data=eval(self.dic["value"]),
                            headers=eval(self.dic["header"]))
        return res

    def __post(self):
        content_type = json.loads(self.dic.get('header')).get('Content-Type')
        if content_type == "application/x-www-form-urlencoded":
            res = requests.post(url=URL + self.dic["interfaceUrl"],
                                data=eval(self.dic["value"]),
                                headers=eval(self.dic["header"]))
        elif content_type == "application/json":
            res = requests.post(url=URL + self.dic["interfaceUrl"],
                                data=eval(self.dic["value"]),
                                headers=eval(self.dic["header"]))
        return res

    def __delete(self):
        res = requests.delete(url=URL+self.dic["interfaceUrl"], params=eval(self.dic["value"]))


if __name__ == '__main__':

    dic1 = {'id': 1.0, 'interfaceUrl': '/user/login', 'name': 'login', 'method': 'post', 'value': "{'username':'liusha','password':'123456'}", 'header': '{"Content-Type": "application/x-www-form-urlencoded","cookie":"${Set-Cookie}"}', 'expect': '0'}
    ch = ConfigHttp(dic1)
    print("========="+dic1["header"])


    result_data = ch.run()
    print(result_data)
    print(result_data.text)
