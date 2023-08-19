"""
http://mr1690712550754.ojqxyuo.cn/coin/index.html?mid=3X6WZJP9V 【元宝阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)
http://mr1690708916508.fgrtlkg.cn/user/index.html?mid=3K7WHTTTC 【花花阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)
http://mr1690711161293.uznmvev.cn/ox/index.html?mid=2B6TJGUDN 【星空阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)

当前脚本支持识别是否是验证文章，如遇到验证文章将返回短链接需手动用未黑号微信打开，此思路将无视黑号，黑号一样有收益

Mr.陈 独家思路😁😁😁😁  @wcnmsb123 有要求可以提但加不加再说😃

新增按照时间来自动选择模式，新增账号详细信息但需在yd值内加上mid值不增也不影响，新增notify青龙推送

变量 moshi= hh/xk/yb 支持三种模式但不支持同时运行
变量 yd={"un":"xxx","token":"xxxx","mid":"xxx"}
如不需要不同时间段自动选择模式，需将下面yxfs值改成""
"""
import time
import random
import requests
import json
import os
import re
import datetime
import configparser
try:
    from notify import send
except:
    pass
yxfs=""  #如不需要不同时间段自动选择模式，需将此值删除
url = "http://u.cocozx.cn/api/"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': "Mozilla/5.0 (Linux; Android 10; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/5583 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'u.cocozx.cn',

    'Connection': 'keep-alive',
}
yu={'Access-Control-Request-Method': 'POST',
    'Content-Length':'113'
}
c={**yu, **headers}
def duanlian(lian):
    headers={"content-type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0 (Linux; Android 12; PEHM00 Build/SKQ1.210216.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1109 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"}
    body={"url":lian}
    url=requests.post("https://aiu.pub/api/link",headers=headers,data=body).json()
    return url["data"]
def huoqu_ydlj(headers,payload,c,yd):
    response = requests.request("OPTIONS", url + yd + "/read", headers=c)
    response = requests.request("post", url +yd+"/read", headers=headers, json=payload).json()
    if response["result"]["status"]==40:
        print("文章还没有准备好",flush=True)
    elif response["result"]["status"]==50:
        print("检测没通过",flush=True)
    elif response["result"]["status"]==60:
        print("已经全部阅读完了",flush=True)
    elif response["result"]["status"] ==70:
        print("下一轮还未开启",flush=True) 
    else:
        try:
           biz=''.join(re.findall('__biz=(.+)&mid',response["result"]["url"]))
           print("阅读链接获取成功", flush=True)
           return biz,response["result"]["url"]
        except:
            biz=""
            return biz
def huoqu_xx(c,payload,yd,mid):
    payload["code"]=mid
    response = requests.request("post", url+yd+"/info", headers=headers, json=payload).json()["result"]
   # print(response)
    print("""[---------账户名%s-----------]\n[---------今日阅读次数%s -----------]\n[---------当前鱼儿%s -----------]\n[---------累计阅读次数%s----------–]"""%(str(response["uid"]),str(response["dayCount"]),str(response["moneyCurrent"]),str(response["doneWx"])),flush=True)
    del payload["code"]
    del c["Content-Length"]
    return
def lingqu_ydjl(headers,payload,c,yd):
    time.sleep(random.randint(6, 8))
    response = requests.request("OPTIONS", url + yd + "/submit", headers=c)
    response = requests.request("post", url +yd+ "/submit", headers=headers, json=payload).json()
    #print(response, flush=True)
    cs = response["result"]["progress"]
    print("阅读成功,当前剩余次数%s"%str(cs), flush=True)
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
    print("当前鱼儿:%s"%str(response))
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
def sj():
    current_time = datetime.datetime.now().time()
    if current_time >= datetime.time(7) and current_time < datetime.time(11):
        yd="user"
    elif current_time >= datetime.time(11) and current_time < datetime.time(17):
        yd="ox"
    elif current_time >= datetime.time(17) and current_time < datetime.time(22):
        yd="coin"
    return yd
# 调用函数
def gg():
    url = requests.get('https://netcut.cn/p/fe616ac873f548ac')
    gg = ''.join(re.findall(r'"note_content":"(.*?)"',url.text)).replace("\\n", "\n")
    print(gg)
    return gg
def zsyx(yxfs,moshi,shuju):
    if yxfs=="zidong":
      print("当前为自动选择模式",flush=True)
      yd=sj()
    else:
      if moshi=="hh":
         yd="user"
      elif moshi=="xk":
         yd = "ox"
      elif moshi=="yb":
         yd = "coin"
    cishu = json.loads(shuju)
    try:
        mid=cishu["mid"]
    except:
        print("mid不存在将不读取账号详细信息",flush=True)
    un = cishu["un"]
    token = cishu["token"]
    payload = {"un": un,
               "token": token,
               "pageSize": "20"
               }
    try:
        huoqu_xx(c,payload,yd,mid)
    except:
        pass
    time.sleep(10)
    print("---------------开始运行模式花花-----------------" if yd=="user" else "---------------开始运行模式元宝----------------" if yd=="coin" else "---------------开始运行模式星空阅读----------------" )
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
            print("--------------------")
            print("遇到检测文章",flush=True)
            time.sleep(1)
            msg=duanlian(biz[1])
            try:
               send("检测文章链接",msg)
               print(msg)
            except:
               print(msg)
            time.sleep(2)
            print("请用未黑号微信打开上面链接,60s后将继续运行",flush=True)
            time.sleep(60)
            print("60s到了",flush=True)
            print("--------------------")
            lingqu_ydjl(headers,payload,c,yd)
            continue
    try:
        tx(headers,payload,c,yd,un,token)
        print("任务完成",flush=True)
    except:
        print("提现失败",flush=True)
cishu=os.getenv('yd').split('&')
for i in range(len(cishu)):
    print(gg())
    print("请确定好前几篇已经手动阅读,10s后将运行程序", flush=True)
    moshi=os.getenv('moshi').split('&')
    zsyx(yxfs,moshi[0],cishu[i])
