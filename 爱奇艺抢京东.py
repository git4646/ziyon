'''
作者TG:@wcnmsb123
作者QQ:2682921363
本脚本无需手动添加code值(因原网络剪切板访问不了，现在专用github)
本人想凑一些爱奇艺v5以上会员,每个月自动开红包内部助力,不用于盈利，如需要联系即可
抓包爱奇艺账号ck里的P00001值放在P00001_values里如多账号用 , 隔开记得每个账号都需要""包裹
'''
import datetime
import concurrent.futures
import requests
import re
import time
target_time = datetime.time(18, 0, 0)#定时时间
P00001_values = [""]  #账号存放区
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
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
def gg():
    url = "https://gh.api.99988866.xyz/https://raw.githubusercontent.com/git4646/ziyon/main/1.txt"
    response = requests.get(url, headers=headers).text
    print(response)
    pattern = r"爱奇艺code:(.+)"  # 正则表达式模式，匹配"爱奇艺code:"后面的数字部分
    code = re.search(pattern, response)
    return code.group(1)
def send_get_pd(P00001):
    url = 'https://tc.vip.iqiyi.com/growthAgency/member-points/points/list'
    params = {
    'P00001': P00001,
    'dfp': '15930d71f71ac34e1ca40d01eb60d3573d59d570b753f1120f901221334df53031',
    'qyid': '7f541020a468f6b2bd523ca0c2c684e51102',
    'version': '14.5.5',
    'agentType': '13',
    'platform': 'bb136ff4276771f3',
    'ptid': '02020031010000000000',
    'fv': 'a30d63890c1c1396',
    'source': 'a30d63890c1c1396',
    '_': '1699934438659',
    'type': '0',
    'pageNo': '1',
    'pageSize': '20'
    }
    response = requests.get(url, headers=headers, params=params).json()["data"][0]
    dt_object = datetime.datetime.fromtimestamp(response["createTime"]//1000)
    formatted_date = dt_object.strftime('%Y %m %d %H:%M:%S')  # 将日期格式化为“xxxx xx xx”
    print("最近一次奖励\n名称:%s\t花费:%s\t时间:%s"%(response["description"],response["totalPoints"],formatted_date))
    return 
def perform_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        msg = data["msg"]
        return response, msg  
def send_get_request(P00001):
    url = 'https://tc.vip.iqiyi.com/growthAgency/v2/growth-aggregation'
    params = {
        'messageId': '564f93c53a3e4cfdb38bd848200913cc',
        'platform': '97ae2982356f69d8',
        'P00001': P00001,
        'responseNodes': 'duration,growth,upgrade,viewTime,growthAnnualCard',
        '_': '1699897908219'
    }
    response = requests.get(url, headers=headers, params=params).json()
    try:
        if response["msg"]=="成功":
            response=response["data"]["user"]
            level=response["level"]
            nickname=response["nickname"]
            deadline=response["deadline"]
            print("会员等级:%s\n账号名称:%s\n到期时间:%s"%(level,nickname,deadline))
    except:
        print("账号失效")
        del P00001_values[P00001]
    return "ok"
code=gg()
base_url = "https://act.vip.iqiyi.com/supermk/seckill/action/seckill?code=%s&P00001=" % code
for value in P00001_values:
    send_get_request(P00001=value)
urls = [base_url + value for value in P00001_values] * 50#定义重发数量

def perform_requests_threadpool(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:  # 控制全部线程最大限度
        results = list(executor.map(perform_request, urls))
    return results

while True:
    current_time = datetime.datetime.now().time()
    if current_time >= target_time:
        results = perform_requests_threadpool(urls)
        for result in results:
            if result:
                response, msg = result
                status_code = response.status_code
                print("Response Code: {}, Message: {}".format(status_code, msg))
        break
for value in P00001_values:
    send_get_pd(P00001=value)        
    