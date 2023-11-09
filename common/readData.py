import json
import os.path
import xlrd2
import yaml

# # 打开excel
# #方式1：根据绝对路径打开
# readbook = xlrd2.open_workbook(r"/Users/liusha/PycharmProjects/pythonProject_InterfaceTest/testData/data.xls")
# print(readbook)
# #方式二：根据相对路径打开
# dirpath = xlrd2.open_workbook(os.path.dirname(os.path.dirname(__file__))+r"/testData/data.xls")
# print(dirpath)
# # 查看所有sheet页的名字
# print(readbook.sheet_names())
# # 获取某个指定的sheet页
# sheet = readbook.sheet_by_index(0)
# # 获取sheet的最大行数和列数
# max_row = sheet.nrows
# max_col = sheet.ncols
# print(max_row, max_col)
# #获取某个单元格的值
# print(sheet.cell_value(1,1))
# #获取某行/列的值
# print(sheet.row_values(1))
# print(sheet.col_values(0))

# #将集合转换成字典，方便取值
# list1 = ["name","age","sex"]
# list2 = ["Tom","18","男"]
# #方式一：推导式实现
# dic1 = {list1[i]:list2[i] for i in range(len(list1))}
# print(dic1)
# #方式二：zip函数转换,转换的是个对象，需要dict转化成字典
# print(dict(zip(list1,list2)))

# 定义一个类
class ReadData:
    # 1.定义init初始化方法
    def __init__(self):
        # 1.1使用相对路径获取文件的路径
        self.path_name = os.path.dirname(os.path.dirname(__file__)) + r"/testData/data.xls"
        # 2.2打开并读取excel
        self.readbook = xlrd2.open_workbook(self.path_name)
        # 1.3获取指定的sheet页
        self.sheet = self.readbook.sheet_by_index(1)
        # 1.4获取最大行/列
        self.max_row = self.sheet.nrows
        self.max_col = self.sheet.ncols
        # 1.5预设一个返回列表，默认为空
        self.res_list = []
        # 1.6获取第一行作为key
        self.first_row = self.sheet.row_values(0)

    # 2.定义一个组装数据的对外方法：read_excel
    def read_excel(self):
        # 循环取出每一行测试数据作为一条测试用例（第一行除外）
        for i in range(1, self.max_row):
            # 2.1获取每一行数据
            row_value = self.sheet.row_values(i)
            # 2.1组装成一个字典
            dict1 = dict(zip(self.first_row, row_value))
            # 2.3将组装好的字典放到列表内
            self.res_list.append(dict1)
        # 2.4返回组装好的结果列表
        return self.res_list

    # 3.定义一个组装数据的对外方法：read_json
    def read_json(self):
        # 3.1获取文件路径
        path_json = os.path.dirname(os.path.dirname(__file__)) + r"/testData/data.json"
        # 3.2打开json文件
        f = open(path_json, "r")
        # 3.3将json转化为字典
        testdata = json.load(f)
        # 3.4关闭json文件
        f.close()
        # 3.5获取字典内所有的value值，转化为列表
        testdata1 = list(testdata.values())
        # 3.6返回组装好的结果
        return testdata1

    # 4.定义一个对外方法：read_yaml
    def read_yaml(self):
        # 4.1获取文件路径
        path_yaml =os.path.dirname(os.path.dirname(__file__)) + r"/testData/data.yaml"
        # 4.2打开yaml文件
        f = open(path_yaml, "r")
        # 4.3读取yaml文件
        testdata = yaml.load(f, Loader=yaml.FullLoader)
        # 4.4关闭yaml文件
        f.close()
        # 4.5返回组装好的数据
        return testdata

if __name__ == '__main__':
    #实例化
    rd = ReadData()
    #调用实例方法
    print(rd.read_excel())
    #print(rd.read_json())
    #print(rd.read_yaml())


