"""
1.配置日志记录器名称
2.配置日志级别
3.配置日志的输出格式(可以分开配置，也可以统一配置)
4.创建并添加handler -控制台
5.创建并添加handler -文件
6.对外提供日志记录器
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志存放路径
log_path = os.path.dirname(os.path.dirname(__file__))+r"/testLog/"


def log():
    # 1.配置日志记录器名称
    logger =logging.getLogger("Test")
    # 2.配置日志级别
    logger.setLevel(logging.DEBUG)
    # 3.配置日志的输出格式(可以分开配置，也可以统一配置)
    format1 = logging.Formatter("日志:%(name)s-级别%(levelname)s-时间%(asctime)s-模块%(module)s.py-第%(lineno)d行:%(message)s")
    # 4.创建并添加handler - 控制台
    sh = logging.StreamHandler()
    sh.setFormatter(format1)
    logger.addHandler(sh)
    # 5.创建并添加handler - 文件
    fh = TimedRotatingFileHandler(filename=log_path+"log", when="D", backupCount=3, encoding="utf-8")
    fh.setFormatter(format1)
    logger.addHandler(fh)
    # 6.对外提供日志记录器
    return logger

# 获取一个日志记录器（单例模式）
logger = log()

if __name__ == '__main__':
    logger.debug("我是debug")
    logger.info("我是info")
    logger.critical("我是灾难")
