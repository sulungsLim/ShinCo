import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import upbit_Auto as uA
import coinTool
import accuracy
import coin_1
import time


uuid = []

while 1:
    
    # 정보 조회
    info = uA.Upbit()

    # 로그인
    upbit_info = info.upbit_info # 로그인 정보
    
    # 매수 필요 정보
    
    base_coin = info.base_coin_name # 설정 코인 이름 정보
    Profit_percent = info.Profit_percent # 수익율 설정 정보
    future_yields = info.base_futuer_yield # 미래가격 대비 수익율 정보
    base_down_price = info.base_down_prices # 설정 코인 매수가 정보
    base_limit_deal_counts = info.base_limit_deal_counts # 설정코인 최소 거래 갯수 정보
    
    
    
    # 매도 필요 정보
    
    up_prices = info.up_prices # 설정 코인 매도가 정보
    now_coin_counts = info.now_coin_counts # 현제 코인 보유 갯수 정보
    now_coin_names = info.now_coin_names
    now_prices = info.now_prices 
    AI_modell_accuracy = info.AI_modell_accuracy
    now_avg_buy_prices = info.now_avg_buy_prices
    
    uuid_count = len(uuid)
    
    if uuid_count == 0:
        
        print('*'*140)
        print('미채결건이 존재하지 않습니다')
        pass
    
    else:
        print('*'*140)
        print('미채결 건수',len(uuid),'건 발생')
        print(uuid)
        
        for i in uuid:
            print(i)
            upbit_info.cancel_order(i)
            
            
            print('*'*140)
            print('미체결 건수 처리 완료')
            
            
        del uuid[:] # 주문ID
    
    
    # 매수 거래 시스템
    
    print('*'*140)
    print( '매수거래가 시작되었습니다' )
    
    for i,coin in enumerate(base_coin):
        print('*'*140)
        print(coin ,'의 거래가 시작됩니다.')
        
        if Profit_percent[1] > future_yields[i] >= Profit_percent[0]:
            
            buy_info = upbit_info.buy_limit_order(coin,base_down_price[i],base_limit_deal_counts[i]*1)
            
            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin,'   ',limit_deal_counts[i]*3,'개 매수 주문 되었습니다')
                
        elif Profit_percent[2] > future_yields[i] >= Profit_percent[1]:
    
            buy_info = upbit_info.buy_limit_order(coin,base_down_price[i],base_limit_deal_counts[i]*2)
            
            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin,'   ',limit_deal_counts[i]*3,'개 매수 주문 되었습니다')
                
        elif future_yields[i] >= Profit_percent[2]:
            
            buy_info = upbit_info.buy_limit_order(coin,base_down_price[i],base_limit_deal_counts[i]*3)
            
            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin,'   ',base_limit_deal_counts[i]*3,'개 매수 주문 되었습니다')
 
    
        print('*'*140)
        print('매도가 시작됩니다')

        for i,count in enumerate(now_coin_counts): #C = [z 개수 > 0 ]
            
            print(now_coin_names[i] ,'의 거래가 시작됩니다.')
            if count > 0 :
                sell_coin = now_coin_names[i]
                sell_event_yield = coinTool.sell_event_yield(now_prices[i],up_prices[i],now_avg_buy_prices[i])
                
                if Profit_percent[1]*AI_modell_accuracy > sell_event_yield >= Profit_percent[0]*AI_modell_accuracy:
                    sell_info = upbit_info.sell_limit_order(sell_coin,up_prices[i],now_coin_counts[i]*(1/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        uuid.append(sell_info[0]['uuid'])
                        print(now_coin_names[i],'   ',now_coin_counts[i]*(1/6),'개 매도주문 하였습니다')
                        
                elif Profit_percent[2]*AI_modell_accuracy > sell_event_yield >= Profit_percent[1]*AI_modell_accuracy:
                    sell_info = upbit_info.sell_limit_order(sell_coin,up_prices[i],now_coin_counts[i]*(2/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        uuid.append(sell_info[0]['uuid'])
                        print(now_coin_names[i],'   ',now_coin_counts[i]*(2/6),'개 매도주문 하였습니다')
                        
                elif Profit_percent[2]*AI_modell_accuracy > sell_event_yield >= Profit_percent[1]*AI_modell_accuracy:
                    sell_info = upbit_info.sell_limit_order(sell_coin,up_prices[i],now_coin_counts[i]*(3/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        uuid.append(sell_info[0]['uuid'])
                        print(now_coin_names[i],'   ',now_coin_counts[i]*(3/6),'개 매도주문 하였습니다')
                
                elif sell_event_yield > 3 :
                    
                    sell_info = upbit_info.sell_limit_order(sell_coin,up_prices[i],now_coin_counts[i])

                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        uuid.append(sell_info[0]['uuid'])
                        print(now_coin_names[i],'전량 매도 하였습니다')
                
                
                elif sell_event_yield < -1 * Profit_percent[2] * 0.25:
                    
                    sell_info = upbit_info.sell_limit_order(sell_coin,up_prices[i],now_coin_counts[i])

                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        uuid.append(sell_info[0]['uuid'])
                        print(now_coin_names[i],'전량 매도 하였습니다')
                        
            print(now_coin_names[i] , '의 거래가 끝났습니다') 
            print('*'*140)
            



    #%%