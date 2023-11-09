"""
1.获取测试数据
2.定义一个测试类
    2.1创建测试用例方法
        2.1.1获取测试数据内进行请求时需要的关键字段
        2.1.2进行请求，获取返回结果
        2.1.3断言返回的实际结果，判断用例中执行成功/失败
"""

import pytest

from common.publicAssertion import PublicAssert
from common.readData import ReadData
from common.configHttp import ConfigHttp
from common.log import logger
from common.preSolve import PreSolve

# 1.获取测试数据
data_obj = ReadData()
# 调用实例方法
test_data = data_obj.read_excel()
# print(test_data)


# 2.定义一个测试类
class TestCase:
    # 2.1创建测试用例方法
    @pytest.mark.parametrize("dic", test_data)
    def test_case(self, dic):
        logger.debug(f"====>{dic}")
        # 判断是否有依赖,执行依赖接口替换依赖字段
        ps = PreSolve(test_data)
        dic["header"], dic["value"] = ps.presolve(dic)
        # 实例化
        ch = ConfigHttp(dic)
        # 调用实例方法
        res = ch.run()
        # 实例化
        pa = PublicAssert(dic, res)
        # 调用实例方法断言
        pa.public_assert()

        # 坑一：用if断言需在失败情况下抛出assertion
        # if str(res_dict["errorCode"]) == str(dic["expect"]):
        #     print("用例执行成功")
        # else:
        #     print("用例执行失败")
        #     raise AssertionError("预期结果与实际结果不符")

        # 坑二：try-except不要加在self.assertEqual前后，否则unittest捕获不到AssertionError,就默认为用例通过
        # try:
        #     assert str(res_dict["errorCode"]) ==str(dic["expect"]), f"预期结果与实际结果不符，预期结果：{dic['except']},实际结果：{res_dict['errorCode']}"
        # except Exception as msg:
        #     print(f"报错信息：{msg}")
        #     raise

        # 将响应的json数据转化成字典
        #res_dict = res.json()
        # 2.1.3断言返回的实际结果，断言用例执行成功/失败
        #assert str(res_dict["errorCode"]) == str(dic["expect"]), f"预期结果与实际结果不符，预期结果：{dic['expect']},实际结果：{res_dict['errorCode']}"


if __name__ == '__main__':
    pytest.main(["-vs"])