import urllib.request
import json
import codecs
import time
import requests
a = []
show_title = 1
# last_date 이전 데이터만 출력
# to_date 이후 데이터만 출력
def get_upbit_data(url, last_date, to_date) :
    global show_title

    fail2GetData = False
    failCnt = 0
    response = ''
    while True:
        try :
            response = requests.get(url)
        except Exception as e:
            print(e)
            time.sleep(20)
            continue
        if str(response) == '<Response [200]>':
            break
        time.sleep(10)
    if ( fail2GetData )  :
        print("Fail to access url")
        exit()

    data = response.json()

    code = data[0]['code']
    if show_title :
      show_title = 0
      print(code)
      print("=========================================================")
      print("          date         open   high   low   final   vol")
      print("=========================================================")

    date = ''
    dateKst = ''
    for i in range(len(data))  :
        dateKst = data[i]['candleDateTimeKst']
        date = data[i]['candleDateTime']
        if (last_date == '' or last_date > date) :
            if (dateKst >= to_date) :
                simpleDate = dateKst.split('+')
                print(simpleDate[0], "%6d"%data[i]['openingPrice'], "%6d"%data[i]['highPrice'], "%6d"%data[i]['lowPrice'], "%6d"%data[i]['tradePrice'], "%9d"%(data[i]['candleAccTradeVolume']));
                a.append(simpleDate[0])
                a.append("%6d"%data[i]['openingPrice'])
                a.append("%6d"%data[i]['highPrice'])
                a.append("%6d"%data[i]['lowPrice'])
                a.append("%6d"%data[i]['tradePrice'])
                a.append(("%9d"%(data[i]['candleAccTradeVolume'])).strip())
            else :
                break

    return date

def get_coin_data_url(coinName, type, scale, cnt=400) :
    addr = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/'
    if type == 'minutes' :
        basic_url = addr + type + '/' + scale + '?code=CRIX.UPBIT.KRW-' + coinName +'&count='+str(cnt)
    else :
        basic_url = addr + type + '/' + '?code=CRIX.UPBIT.KRW-' + coinName +'&count='+str(cnt)

    return basic_url

# 수정 변수들
    
coinName = "ETH"; # 코인명 설정


to_date = '2018-02-01' # 날짜 설정
type = 'minutes'  #minutes/#, days, weeks, months
scale = '15' #단위 설정
# 수정 변수들 끝

end = 0

last_date = ''  #last_date = '2019-09-05T16:37:00+09:00'
basic_url = get_coin_data_url(coinName, type, scale)
url = basic_url

while (1) :
    last_date = get_upbit_data(url, last_date, to_date)
    tmp1 = last_date.split('T')
    if tmp1[0]  < to_date :
        break
    tmp2 = tmp1[1].split('+')
    target_date = tmp1[0] + ' ' + tmp2[0]
    url = basic_url + '&to=' + target_date    #to=2019-11-27 04:01:00
    time.sleep(3)
    

print('')

import numpy as np

b = np.array(a)


b1 = b.reshape(-1,6)



import pandas as pd

df = pd.DataFrame(b1,columns = ['date','open','high','low','final','vol']) # 컬럼 설정



df.to_csv('d:\\ETH_15mm_(2018-02-01 ~ 2020-3-16)_columns.csv', header=True, index=False) #저장 파일 설정


    



























