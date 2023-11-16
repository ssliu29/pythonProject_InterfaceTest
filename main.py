# 执行测试用例生成测试报告
import json
import shutil

import pytest
import os
import time
from common.sendEmail import SendEmail

"""
设置报告窗口的标题：set-window_title
    1.以读写的方式打开index.html文件，保存到对象f内
    1.1 获取当前文件所有内容
    1.2 把指针挪到开始位置
    1.3 截断文件
    1.4 循环遍历每一个"Allure Report"替换为新的标题
    
修改报告内标题：config_title
获取summary.json文件的数据内容
    以只读模式打开并保存到f内
    加载json文件内容给变量params
    修改内容
    将修改后的内容保存在字典内
    以写的方式再次打开该文件，并写入修改后的数据
    将修改后的字典写入到文件内
    
清理报告：auto_clear
全部清理：
    os.listdir()获取目录下所有文件名得到一个列表
        循环删除每一个列表
"""

# 设置报告窗口的标题：set-window_title
def set_window_title(new_title, file_path):
    # 1. 以读写的方式打开index.html文件，保存到对象f内
    with open(file_path + r"/index.html", 'r+', encoding="utf-8") as f:
        # 1.1 获取当前文件所有内容
        all_the_lines = f.readlines()
        # 1.2 把指针挪到开始位置
        f.seek(0)
        # 1.3 截断文件
        f.truncate()
        # 1.4 循环遍历每一个"Allure Report""替换为新的标题
        for line in all_the_lines:
            f.write(line.replace("Allure Report", new_title))

# 修改报告内标题：config_title
def config_title(name, file_path):
    # 获取summary.json文件的数据内容
    file_path = file_path + r"/widgets/summary.json"
    # 以只读模式打开并保存到f内
    with open(file_path, "rb") as f:
        # 加载json文件内容给变量params
        params = json.load(f)
        # 修改内容
        params["reportName"] = name
        # 将修改后的内容保存在字典内
        dict1 = params
        # 以写的方式再次打开该文件，并写入修改后的数据
    with open(file_path, "w", encoding="utf-8") as r:
        # 将修改后的字典写入到文件内
        json.dump(dict1, r, ensure_ascii=False, indent=4)

# 全部报告：
def auto_clear(n):
    # 删除临时文件目录
    shutil.rmtree(os.path.dirname(__file__)+r"/testReport/temp")
    # os.listdir()获取目录下所有文件名得到一个列表
    dir = os.path.dirname(__file__)+r"/testReport/"
    file_list = os.listdir(dir)
    file_list.sort(key=lambda x: os.path.getctime(dir+x))
    print(file_list)
    # 循环删除每一个列表
    for i in file_list[:-n]:
        shutil.rmtree(dir + i)

if __name__ == '__main__':
    # 获取当前时间并拼接到测试报告内
    cur_time = time.strftime("%Y_%m_%d_%H_%S", time.localtime())
    report = os.path.dirname(__file__) + r"/testReport/"+cur_time

    # 执行测试用例，生成临时报告
    pytest.main()
    # 将临时报告转化成为真正的allure报告
    os.system("allure generate ./testReport/temp -o " + report)
    # 修改窗口标题
    set_window_title("接口自动化测试报告", report)
    # 修改报告内标题
    config_title("自动化报告内标题", report)
    # 创建一个查看结果的插件
    with open(report+r"/请点我打开报告.bat", "w", encoding="utf-8") as f:
        f.write(r"allure open ./")
    # 将报告压缩成zip包，并返回压缩的完的路径
    zip_dir = shutil.make_archive(base_name="./testReport/temp/测试报告", format="zip", root_dir=report)
    print(zip_dir)
    # 发送报告
    se = SendEmail()
    se.send(zip_dir)
    # 清理报告
    #auto_clear(4)
