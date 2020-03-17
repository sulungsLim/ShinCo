import pyupbit
import numpy as np
import pandas as pd
import coinTool
from accuracy import Prediction
import time


class Upbit(Prediction):
    
    
    def __init__(self):
        
        super().__init__()
        
        
        self.Profit_percent = [0.7 , 1 , 1.5]#수익율 단위
        self.AI_modell_accuracy = 0.8 # 정확도
        
        
        self.now_coin_names = [] # 현재 코인 종류
        self.now_prices = [] # 코인별 현재 가격
        self.now_coin_counts = [] # 코인별 보유 갯수
        self.now_avg_buy_prices = [] # 평균 매수 가격
        self.future_yields = [] # 수익율 
        self.limit_deal_counts = [] #최소거래 갯수
        self.up_prices = [] # 매도 호가
        self.down_prices = [] # 매수 호가
        self.coin_yields = [] # 코인별 수익율
        
        self.base_future_yield = []
        self.base_coin_now_price = []
        self.base_futuer_yield = []
        self.base_up_prices = [] # 매도 호가
        self.base_down_prices = [] # 매수 호가
        self.base_limit_deal_counts = [] #최소거래 갯수
        
        
        
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        
        #time.sleep(3)
        
        #self.uncollected()
        self.account_clear()
        
        #self.future_prices = []
        self.login_key()
        self.upbit_login()
        self.account_info() #계좌 정보 가져오기
        self.base_data_info()
        self.account_inquiry() # 정보 조회
        self.my_account_data_info() # 판다스 통계 출력
        
        #time.sleep(3)
        
       
    def login_key(self):
           
        self.access_key = 'jlY7Psx9dJHRSsHE0rO8HGllu8cj954AvwwZwBgy'
        self.secret_key = '62noVvWuHZpqFKXZyQaEG5lbeg1D1uI19Y8t4Smx'

  
    def upbit_login(self):
        
        
        upbit = pyupbit.exchange_api.Upbit(self.access_key, self.secret_key)
        self.upbit_info = upbit
        

       
    def account_info(self):    
    
        self.user_info_ = self.upbit_info.get_balances()[0]
        my_info = self.user_info_[0]
        my_info_price = my_info['balance']
                
        #uuid_count = len(self.uuid)
        print('='*120)
        print('현재 보유 자산 : ', my_info_price)
        #print('전 싸이클 거래 요청 건수 : ', uuid_count)

    
    def uuid(self):
        self.uuid = []   # 미채결 항목
        
    def uncollected(self):

        uuid_count = len(self.uuid)
        
        if uuid_count == 0:
            print('='*140)
            print('미채결건이 존재하지 않습니다')
            pass
        
        else:
            print('미채결 건수 발생')
            
            for i in self.uuid:
                
                self.upbit_info.cancel_order(i)
                print('미체결 건수 처리 완료')
                del self.uuid[:] # 주문ID
    

            

    def account_inquiry(self):
        
        coin_count = len(self.user_info_) - 1  #코인 보유 갯수수

        for i in range(coin_count):
            coin_info = self.user_info_[i+1] # 보유하고 있는 코인 정보를 1개씩 가져온다.
            
            coin_name = coin_info['currency']
            coin_count = coin_info['balance']
            coin_avg_price = coin_info['avg_buy_price']
            coin_type = coin_info['unit_currency']
            now_price = pyupbit.get_current_price(coin_type + '-' + coin_name)
            orderbook = pyupbit.get_orderbook(coin_type + '-' + coin_name)
            bids_asks = orderbook[0]['orderbook_units']
            down_price = bids_asks[0]['bid_price']
            up_price = bids_asks[0]['ask_price']
            future_yield = coinTool.price_yield(now_price, self.future_price_LSTM[i])
            limit_count = coinTool.limit_deal_count(now_price)
            coin_yield = coinTool.sell_event_yield(float(up_price),float(up_price),float(coin_avg_price))
            
            self.coin_yields.append(coin_yield)
            self.up_prices.append(float(up_price))
            self.down_prices.append(float(down_price))
            self.future_yields.append(float(future_yield))
            self.now_coin_names.append(coin_type + '-' + coin_name)
            self.now_coin_counts.append(float(coin_count))
            self.now_avg_buy_prices.append(float(coin_avg_price))
            self.now_prices.append(float(now_price))
            self.limit_deal_counts.append(float(limit_count))
    
    def base_data_info(self):
        
        base_count = len(self.base_coin_name)
        
        for i in range(base_count):

            base_now_price = pyupbit.get_current_price(self.base_coin_name[i])
            self.base_coin_now_price.append(base_now_price)
            
            future_yield = coinTool.price_yield(base_now_price, self.base_future_price_LSTM[i])
            self.base_futuer_yield.append(future_yield)
            
            limit_count = coinTool.limit_deal_count(base_now_price)
            self.base_limit_deal_counts.append(float(limit_count))
            
        
            
            a = pyupbit.get_orderbook(tickers = self.base_coin_name[i])
            a1 = a[0]['orderbook_units']
            down_price = a1[0]['bid_price']
            up_price = a1[0]['ask_price']
            self.base_up_prices.append(float(up_price))
            self.base_down_prices.append(float(down_price))
            

    def my_account_data_info(self):

      
        
        df_1 = [self.now_prices,self.coin_yields,self.now_coin_counts,self.now_avg_buy_prices,self.future_price_LSTM,
              self.future_yields,self.limit_deal_counts,self.up_prices,self.down_prices]
        
        df_1 = np.array(df_1)

      
        df1 = pd.DataFrame(df_1,columns = [self.now_coin_names],
                              index = ['now_price','coin_yields','coin_count','avg_buy_prices','future_price_LSTM',
                                       'future_yields','limit_count','up_price','down_price']).T
        
        df_2 = [self.base_coin_now_price,self.base_future_price_LSTM,self.base_futuer_yield,
                self.base_limit_deal_counts,self.base_up_prices,self.base_down_prices]
        df_2 = np.array(df_2)

        
        df2 = pd.DataFrame(df_2,columns = [self.base_coin_name],
                              index = ['now_price','future_price_LSTM',
                                       'future_yields','limit_count','up_price','down_price']).T
        
        

        print('*'*140)
        print('코인 예측율 및 정보들')
        print(df2)
        print('*'*140)
        print('현재 보유 코인 개수:',len(self.now_coin_names))
        print(df1)
        print('='*140)

    
    def account_clear(self):
        
        del self.now_coin_names[:] # 현재 코인 종류
        del self.now_prices[:] # 코인별 현재 가격
        del self.now_coin_counts[:] # 코인별 보유 갯수
        del self.now_avg_buy_prices[:] # 평균 매수 가격
        del self.future_yields[:] # 수익율 
        del self.limit_deal_counts[:] #최소거래 갯수
        del self.up_prices[:] # 매도 호가
        del self.down_prices[:] # 매수 호가
        


class Buying(Upbit):
    
    def __init__(self):
        
        super().__init__()
        self.buy_run()
        
    
    def buy_run(self):
        
        print('매수거래가 시작되었습니다.')
        for i,coin in enumerate(self.now_coin_names):
            
            if self.Profit_percent[1] > self.future_yields[i] >= self.Profit_percent[0]:
                
                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*3)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])
                    print(coin,self.limit_deal_counts[i]*3,'개 매수 주문 되었습니다')
                    
            elif self.Profit_percent[2] > self.future_yields[i] >= self.Profit_percent[1]:

                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*6)
                print(buy_info)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])
                    print(coin,self.limit_deal_counts[i]*3,'개 매수 주문 되었습니다')
                    
            elif self.future_yields[i] >= self.Profit_percent[2]:
                
                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*9)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])
                    print(coin,self.limit_deal_counts[i]*3,'개 매수 주문 되었습니다')



class Selling(Buying):# 매도
    
    def __init__(self):
        super().__init__()
        self.sell_run()
        
        
    def sell_run(self):

        print('매도가 시작됩니다')
        for i,count in enumerate(self.now_coin_counts): #C = [z 개수 > 0 ]
            print(self.now_coin_names[i] ,'의 거래가 시작됩니다.')
            if count > 0 :
                sell_coin = self.now_coin_names[i]
                sell_event_yield = coinTool.sell_event_yield(self.now_prices[i],self.up_prices[i],self.now_avg_buy_prices[i])
                
                if self.Profit_percent[1]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[0]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_counts[i]*(1/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        print(self.now_coin_names[i],'   ',self.now_coin_counts[i]*(1/6),'개 매도주문 하였습니다')
                        
                elif self.Profit_percent[2]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[1]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_counts[i]*(2/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        print(self.now_coin_names[i],'   ',self.now_coin_counts[i]*(2/6),'개 매도주문 하였습니다')
                        
                elif self.Profit_percent[2]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[1]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_counts[i]*(3/6))

                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        print(self.now_coin_names[i],'   ',self.now_coin_counts[i]*(3/6),'개 매도주문 하였습니다')
                
                elif sell_event_yield < -self.Profit_percent[2] * 0.25:
                    
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_counts[i])

                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        print(self.now_coin_names[i],'전량 매도 하였습니다')
            print(self.now_coin_names[i] , '의 거래가 끝났습니다') 
            print('*'*120)
                    
            

# 1분동 15분본 60분봉 으로 각각 예측 정확도를 테스트 실험테스트 하면서 결과를 저장해야된다.           
                


#예측율 업데이트
#예측 평가
#종목 선정
    