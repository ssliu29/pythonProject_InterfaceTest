"""
创建一个类
1.定义初始化方法
    1.1获取配置文件的路径
    1.2实例化congfigpraser类
    1.3读取指定路径下的文件
    1.4查看当前配置文件下所有section
2.创建一个对外方法：
    如果参数只有一个，则获取这个section下面所有的option的键值对
    如果参数有2个，则获取这个section下面的指定的option的值
"""

import os.path
from configparser import ConfigParser

class ReadConfig:
    # 1.定义初始化方法
    def __init__(self):
        # 1.1获取配置文件的路径
        self.path =os.path.dirname(os.path.dirname(__file__)) + r"/config.ini"
        # 1.2实例化congfigpraser类
        self.conf = ConfigParser()
        # 1.3读取指定路径下的文件
        self.conf.read(self.path, encoding="utf-8")
        # 1.4查看当前配置文件下所有section
        self.sections = self.conf.sections()
        print(self.sections)

    # 2.定义一个对外方法：
    def get_config(self, section, option="all"):
        # 如果参数只有一个，则获取这个section下面所有的option的键值对
        if option == "all":
            return self.conf.items(section)
        # 如果参数有2个，则获取这个section下面的指定的option的值
        else:
            return self.conf.get(section, option)

if __name__ == '__main__':
    rc = ReadConfig()
    print(rc.get_config("mysql"))
    print(rc.get_config("redis", "port"))