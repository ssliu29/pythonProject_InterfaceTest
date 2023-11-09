import requests


url1 = "https://www.wanandroid.com/user/login"

payload = {"username": "liusha", "password": "123456"}

res = requests.post(url=url1, data=payload)

# 查看状态码
print(res.status_code)

# 查看响应体
print(res.content)
print("------------------")
# 将cookie存放到变量中
cookie = res.cookies
print(cookie)
print("=======================")

url2 = "https://www.wanandroid.com/user/lg/userinfo/json"

res2 = requests.get(url=url2, cookies=cookie)
print(res2.text)


