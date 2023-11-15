import requests
import json
import re
x_P00001="2dUuuXfC6Ghm27V5wiAB2hVIrWc3r57m2bOk3vZQeQcnYo4Ts1bADc7T6QkofXeSZLm3W57"
y_P00001=[]
for i in range(int(input("几个账号:"))):
    y_P00001.append(input("输入开包者P00001:"))
headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 IqiyiApp/iqiyi IqiyiVersion/14.5.5 IqiyiPlatform/2_22_222 QYStyleModel/(light)',
        'origin': 'https://vip.iqiyi.com',
        'x-requested-with': 'com.qiyi.video',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://vip.iqiyi.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
def kai_hb(P00001):
    url = 'https://act.vip.iqiyi.com/level-right/red/gen'
    params = {
        'P00001': P00001,
        'fv':'896ec1a1fb1ee09a'
    }
    response = requests.get(url, headers=headers, params=params).json()
    try:
        redNo=response["data"]["redNo"]
        return redNo
    except:
        return "已开"    
def cx_hb(P00001):
    url = 'https://act.vip.iqiyi.com/level-right/red/status'
    params = {
        'P00001': P00001
    }
    response = requests.get(url, headers=headers, params=params).json()
    redNo=response["data"][0]["redNo"]
    return redNo
def send_get_request(redNo,P00001):
    url = 'https://act.vip.iqiyi.com/bonus/api/grabRed'
    params = {
    'redNo': redNo,
    'accountType': '2',
    'P00001': P00001,
    '_': '1699703121685',
    'callback': 'Zepto1699703121151'
    }
    response=(requests.get(url, headers=headers, params=params).text)
    json_match = re.search(r'window\.Zepto\d+\((\{.*\})\)', response)
    json_text = json_match.group(1)
    # 解析提取到的 JSON 数据
    data = (json.loads(json_text))["data"]
    if data["msg"]!="已抢过":
       print("账号:%s\t获得%s天"%(data["data"]["mobile"],data["data"]["giftList"][0]["receiveDays"]))
    else:
        print("账号:%s 已抢过"%(data["data"]["mobile"]))
    return
for P00001 in y_P00001:
    try:
       redNo=kai_hb(P00001)
       if redNo=="已开":
          redNo=cx_hb(P00001)
       send_get_request(redNo,x_P00001)
    except:
        print('账号失效')   

