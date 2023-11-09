"""
思路分析
定义一个类：DingTalk
1.定义初始化方法
    1.1 创建一个请求头并确定为实例属性
    1.2将请求地址绑定为实例属性
2. 定义对外发送普通信息的方法：send_msg
    2.1定义发信息所需的参数
    2.2定义发送信息请求
3.定义对外发送普通信息的方法：send_link
    3.1定义发信息所需的参数
    3.2定义发送信息请求
"""

import requests

class DingTalk:
    # 1.定义初始化方法
    def __init__(self):
        # 1.1创建一个请求头并确定为实例属性
        self.__haeders = {'Content-Type': 'application/json;charset=utf-8'}
        # 1.2将请求地址绑定为实例属性
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=ded597142fbee3889e19d9b1ecc06ad89b7b91c7bbc55fd30c38ba06f5f46818'

    # 2.定义对外发送普通信息的方法：send_msg
    def send_msg(self, text):
        # 2.1定义发信息所需的参数
        dic = {
            "msgtype": "text",
            "text": {"content": text},
            "at": {
                "atMobiles": ["+86-13552828809", "+86-18601916518"],
                "isAtall": False
            }
        }
        # 2.2定义发送信息请求
        requests.post(self.url, json=dic, headers=self.__haeders)
        return "发送成功"

    def send_link(self,text,url):
        # 3.1定义发信息所需的参数
        dic = {
            "msgtype":"link",
            "link": {
                "text": text,
                "title": "登录模块测试报告，请查收",
                "messageUrl": url
            }
        }
        # 3.2定义发送信息请求
        requests.post(self.url, json=dic, headers=self.__haeders)
        return "发送成功"

if __name__ == '__main__':
    dt = DingTalk()
    print(dt.send_msg("测试：我是大聪明"))
    print(dt.send_link("测试报告：", "https://www.baidu.com/"))