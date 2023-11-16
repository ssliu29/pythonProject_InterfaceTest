# 公共断言
"""
定义一个类
1.定义初始化方法
    1.1获取用例预期结果
    1.2获取返回的实际结果
    1.3获取返回的状态码

2.定义一个对外的断言方法
    2.1断言状态码是否正确
    2.2循环断言字典里的键值对
        2.2.1根据获取出来的键获取返回结果内的预期结果
        2.2.2断言取到的实际结果和预期结果是否相同
"""

from jsonpath import jsonpath

class PublicAssert:
    # 1.定义初始化方法：
    def __init__(self, dic, res):
        # 1.1获取用例预期结果
        self.expect = eval(dic["expect"])
        # 1.2获取返回的实际结果
        self.res = res.json()
        # 1.3获取返回的状态码
        self.status_code = res.status_code

    # 2.定义一个对外的断言方法
    def public_assert(self):
        # 2.1断言状态码是否正确
        assert self.status_code in [200, 304], f"请求失败响应状态码为:{self.status_code}"
        # 2.2循环断言字典里的键值对
        for k, v in self.expect.items():
            # 2.2.1根据取出的键获取返回结果内预期结果
            print(f"预期结果:{k}:{v}")
            real = jsonpath(self.res, "$.."+k)[0]
            # 2.2.2断言取到的实际结果和预期结果是否相同
            assert str(real) == str(v), f"预期结果与实际不符合：预期结果{str(v)},实际结果{str(real)}"

if __name__ == '__main__':
    from common.readData import ReadData
    from common.configHttp import ConfigHttp
    data = ReadData().read_excel()
    ch = ConfigHttp(data[0])
    res1 = ch.run()
    print(res1.text)
    # 调用当前类
    pa = PublicAssert(data[0], res1)
    pa.public_assert()