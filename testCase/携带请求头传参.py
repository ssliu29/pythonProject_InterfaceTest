import requests

url1 = "https://www.wanandroid.com/user/login"
payload = {"username":"liusha","password":"123456"}
res = requests.post(url=url1, data=payload)
# 查看响应体
print(res.text)

#将cookie存放在变量中
cookie = res.cookies
print(res.headers)
print(cookie)
print("+++++++++++++++++++++++")

#手写一个请求头
header = {}
header["Cookie"] = res.headers["Set-Cookie"]
print(header)
#准备接口
url2 = "https://www.wanandroid.com/user/lg/userinfo/json"

res2 = requests.get(url=url2, headers=header)
print(res2.text)
