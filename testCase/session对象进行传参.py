import requests

url1 = "https://www.wanandroid.com/user/login"
payload = {"username":"liusha","password":"123456"}
# 创建一个session对象
s = requests.session()
# 用session对象s进行请求并保存请求结果
res = s.post(url=url1, data=payload)
# 查看响应体
print(res.text)
print("======================")

url2 = "https://www.wanandroid.com/user/lg/userinfo/json"

res2 = s.get(url=url2)
print(res2.text)