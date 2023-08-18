"""
http://mr1690712550754.ojqxyuo.cn/coin/index.html?mid=3X6WZJP9V 【元宝阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)
http://mr1690708916508.fgrtlkg.cn/user/index.html?mid=3K7WHTTTC 【花花阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)
http://mr1690711161293.uznmvev.cn/ox/index.html?mid=2B6TJGUDN 【星空阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)

当前脚本支持识别是否是验证文章，如遇到验证文章将返回短链接需手动用未黑号微信打开，此思路将无视黑号，黑号一样有收益

Mr.陈 独家思路😁😁😁😁

变量 moshi= hh/xk/yb 支持三种模式但不支持同时运行
变量 yd={"un":"xxx","token":"xxxx"}
"""
import time
import random
import requests
import json
import os
import re
import configparser
url = "http://u.cocozx.cn/api/"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': "Mozilla/5.0 (Linux; Android 10; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/5583 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'u.cocozx.cn',
    'Connection': 'keep-alive',
}
yu={'Access-Control-Request-Method': 'POST'}
c={**yu, **headers}
def duanlian(lian):
    headers={"content-type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0 (Linux; Android 12; PEHM00 Build/SKQ1.210216.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1109 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"}
    body={"url":lian}
    url=requests.post("https://aiu.pub/api/link",headers=headers,data=body).json()
    return url["data"]
def wx_get(biz):
    wx={
    "user-agent":"Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5197 MMWEBSDK/20230504 MMWEBID/1942 MicroMessenger/8.0.37.2380(0x2800255B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Cookie":"rewardsn=;wxtokenkey=777;wxuin=1943218360;devicetype=android-31;version=2800255b;lang=zh_CN;appmsg_token=1229_Oqcy%2B%2F03B3mXKoMtfDglh-94EM-40l43ceSYg1Hs1zYzW8BnAqBXG2cZ_9BHH5Jef7Ynlx_VnvvpT2mB;pass_ticket=5mcaQMujUY4IQu1/52gJhpUQ7kEn0X8ZzLh7nSlEyQ0RK8oDQf1xOr1xknFGATye;wap_sid2=CLjRzJ4HErYBeV9IRHNhMGV4WDlheWtjcTQxNGczRWZrR3F2V2NxWVo3bXFxeU0xNEFOUWt4Q0I0cFVXT1Q1cGNCRnM3d3JEYkEyT3VKZjRUYWhYSkVEa0JkRlpYMlV5cFZJM0NBVlNodW5sbnJhckN6UWNpSW9mVzBrQUJ1MDJOY0dXbDZIN2phQzlTbFBzWWNtODBvN3MtWE9Wb1poRGgtX2xNRU9XMGtsNEhNMG5ENzZIMEhBcWhJQUFBfn4w8YWupgY4DUAB"
}
    url=requests.get(biz,headers=wx)
    return
def huoqu_ydlj(headers,payload,c,yd):
    response = requests.request("OPTIONS", url + yd + "/read", headers=c)
    response = requests.request("post", url +yd+"/read", headers=headers, json=payload).json()
    try:
       biz=''.join(re.findall('__biz=(.+)&mid',response["result"]["url"]))
       print(response, flush=True)
       return biz,response["result"]["url"]
    except:
        print("检测没通过",flush=True)
        biz=""
        return biz
def lingqu_ydjl(headers,payload,c,yd):
    time.sleep(random.randint(6, 8))
    response = requests.request("OPTIONS", url + yd + "/submit", headers=c)
    response = requests.request("post", url +yd+ "/submit", headers=headers, json=payload).json()
    #print(response, flush=True)
    cs = response["result"]["progress"]
    return cs

def tx(headers,payload,c,yd,un,token):
    money=xinxi(headers,payload,c,yd)
    print("提现金额:"+money)
    payload = {"val":money,
               "un": un,
               "token": token,
               "pageSize": "20"
               }
    if yd=="user":
        tx_moshi="/wd"
    else:
        tx_moshi="/wdmoney"
    response = requests.request("OPTIONS", url + yd +tx_moshi, headers=c)
    response = requests.request("post", url +yd+tx_moshi, headers=headers, json=payload).json()
    print(response)
    return 
def xinxi(headers,payload,c,yd):
    response = requests.request("OPTIONS", url +yd+"/info", headers=c)
    response = requests.request("post", url+yd+"/info", headers=headers, json=payload).json()
    print(response)
    money=int((response["result"]["moneyCurrent"]))
    print(money)
    if 3000<money<4999:
        money="3000"
    elif 5000<money<9999:
        money="5000"
    elif 10000<money<49999:
        money="10000"
    elif money>=50000:
        money="50000"
    return money
def zsyx(moshi,shuju):
    if moshi=="hh":
        yd="user"
    elif moshi=="xk":
        yd = "ox"
    elif moshi=="yb":
        yd = "coin"
    print("---------------开始运行模式花花----------------------" if yd=="user" else "---------------开始运行模式元宝----------------------" if yd=="coin" else "---------------开始运行模式星空阅读----------------------" )
    cishu = json.loads(shuju)
    print(cishu)
    un = cishu["un"]
    token = cishu["token"]
    payload = {"un": un,
               "token": token,
               "pageSize": "20"
               }
    while True:
        biz=huoqu_ydlj(headers,payload,c,yd)
        time.sleep(3)
        if biz=="":
          break
        elif biz[0]!="Mzg2Mzk3Mjk5NQ==":
            try:
                result = lingqu_ydjl(headers,payload,c,yd)
                if result != 2:
                    continue
                else:
                    break
            except:
                break
        else:
            print("遇到检测文章",flush=True)
            time.sleep(1)
            print(duanlian(biz[1]))
            time.sleep(2)
            print("请用未黑号微信打开上面链接,60s后将继续运行",flush=True)
            time.sleep(60)
            print("60s到了",flush=True)
            lingqu_ydjl(headers,payload,c,yd)
            continue
    try:
        tx(headers,payload,c,yd,un,token)
        print("任务完成",flush=True)
    except:
        print("提现失败",flush=True)
cishu=os.getenv('yd').split('&')
for i in range(len(cishu)):
    print("请确定好前几篇已经手动阅读,10s后将运行程序", flush=True)
    time.sleep(10)
    cishu=os.getenv('yd').split('&')
    moshi=os.getenv('moshi').split('&')
    zsyx(moshi[0],cishu[i])