# 数据依赖
"""
定义一个类
1.定义初始化方法
1.1 获取所有测试用例数据并绑定为实例方法

2. 定义一个方法：根据当前用例的id,执行依赖的前置用例并替换依赖字段header，body
2.1 获取用于判断是否有前置用例的关键字段：rely,caseid,header,value
2.2 判断是否有前置用例，判断caseid是否有值？
    2.2.1 有依赖：根据正则找出请求头/体里面依赖的字段：可以封装成一个单独的方法进行调用
    2.2.2 执行前置用例得到前置用例的返回结果，在结果内根据上一步获取得到的依赖字段获取响应里的实际数据：封装成一个独立方法进行调用
    2.2.3 获取到的依赖字段实际结果，替换原来的数据
    2.2.4 返回替换好的header和value
2.3 没有依赖：返回当前的header和value

3.定义一个方法：提取需要依赖的请求头/体里的
    3.1根据正则提取依赖字段，得到一个列表
    3.2 判断得到的列表是否有数据
        3.2.1 是：返回依赖字段
        3.2.2 否：返回None

4. 定义一个方法：执行前置用例，根据准备好的目标字段提取实际的数据：响应头/响应体
    4.1准备前置用例请求所需要的数据
    4.2 调用configHttp进行接口请求,并得到返回值
    4.3 判断请求头里面是否有依赖字段，有则返回依赖的数据
    4.4 判断请求体里面是否有依赖的字段，有则返回依赖数据
    4.5 返回得到的依赖字段
"""
import re

from jsonpath import jsonpath

from common.configHttp import ConfigHttp
from common.log import logger


# 定义一个类
class PreSolve:
    # 1.定义初始化方法
    def __init__(self, testdata):
        # 1.1 获取所有测试用例数据并绑定为实例方法
        self.testdata = testdata

    # 2. 定义一个方法：根据当前用例的id,执行依赖的前置用例并替换依赖字段header，body
    def presolve(self, dic):
        # 2.1 获取用于判断是否有前置用例的关键字段：rely,caseid,header,value
        rely = dic["rely"]
        caseid = dic["caseid"]
        header = dic["header"]
        value = dic["value"]
        logger.debug(f"关键字段：{rely},{caseid},{header},{value}")
        # 2.2 判断是否有前置用例，判断caseid是否有值？
        if rely.lower() == "y" and caseid != "":
            # 2.2.1 有依赖：根据正则找出请求头/体里面依赖的字段：可以封装成一个单独的方法进行调用
            goal_header = self.get_predata(header)
            goal_body = self.get_predata(value)
            logger.debug(f"请求头里面的依赖字段：{goal_header},请求体里面依赖的字段：{goal_body}")
            # 2.2.2 执行前置用例得到前置用例的返回结果，在结果内根据上一步获取得到的依赖字段获取响应里的实际数据：封装成一个独立方法进行调用
            h,b = self.run_pre(caseid,goal_header,goal_body)
            logger.debug(f"实际请求头里面的依赖字段：{h},体里面的实际依赖字段：{b}")
            # 2.2.3 获取到的依赖字段实际结果，替换原来的数据
            if h != None:
                header = header.replace("${"+goal_header+"}", h)
            # 2.2.4 返回替换好的header和value
            if b != None:
                value = value.replace("${"+goal_body+"}", b)
            return header,value
        # 2.3 没有依赖：返回当前的header和value
        else:
            return header, value

    # 3.定义一个方法：提取需要依赖的请求头/体里的
    def get_predata(self,data):
        # 3.1根据正则提取依赖字段，得到一个列表
        res = re.findall(r"\${(.*?)}", str(data))
        # 3.2 判断得到的列表是否有数据
        if len(res) != 0:
            # 3.2.1 是：返回依赖字段
            return res[0]
        # 3.2.2 否：返回None
        else:
            return None

    # 4. 定义一个方法：执行前置用例，根据准备好的目标字段提取实际的数据：响应头/响应体
    def run_pre(self, caseid, goal_header = None,goal_body =None):
        # 4.1准备前置用例请求所需要的数据
        data = self.testdata[int(caseid)-1]
        # 4.2 调用configHttp进行接口请求,并得到返回值
        ch = ConfigHttp(data)
        res = ch.run()
        logger.debug(f"依赖的字段：header:{goal_header},body:{goal_body}")
        logger.debug(f"执行的结果：{res.text}")
        # 4.3 判断请求头里面是否有依赖字段，有则返回依赖的数据
        if goal_header != None:
            goal_header = res.headers[goal_header]
            print("请求头取到的实际依赖结果",goal_header)
        # 4.4 判断请求体里面是否有依赖的字段，有则返回依赖数据
        if goal_body != None:
            goal_body = jsonpath(res.json(), "$.."+goal_body)[0]
            print("请求体取到的实际依赖结果", goal_body)
        # 4.5 返回得到的依赖字段
        return goal_header,goal_body


if __name__ == '__main__':
    from common.readData import ReadData
    data = ReadData().read_excel()
    print(data)
    # 调试当前类
    ps = PreSolve(data)
    print(ps.presolve(data[4]))
    # 测试数据
    # str1 = {'name':'${username}','link':'www.baidu.com'}
    # print(ps.get_predata(str1))
    # print(ps.run_pre("1","Set-Cookie","username"))