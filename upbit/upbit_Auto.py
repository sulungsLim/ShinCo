import pyupbit
import numpy as np
import pandas as pd
import coinTool
import accuracy


class Upbit:
    
    def __init__(self):

        self.Profit_percent = [0.7 , 1 , 1.5]#수익율 단위
        self.future_prices = accuracy.data_maker.accuracy_evaluation() # 예측가격
        self.AI_modell_accuracy = [0.8] # 정확도
        
        self.uuid = []     # 미채결 항목
        
        self.now_coin_names = [] # 현재 코인 종류
        self.now_prices = [] # 코인별 현재 가격
        self.now_coin_counts = [] # 코인별 보유 갯수
        self.now_avg_buy_prices = [] # 평균 매수 가격
        self.future_yields = [] # 수익율 
        self.limit_deal_counts = [] #최소거래 갯수
        self.up_prices = [] # 매도 호가
        self.down_prices = [] # 매수 호가
        
        
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        
        self.login_key()
        self.upbit_login(self.access_key, self.secret_key)
        self.account_info(self.upbit_info,self.uuid,self.future_prices)
        self.my_account_data_info()
        

        
    def login_key(self):
           
        self.access_key = 'jlY7Psx9dJHRSsHE0rO8HGllu8cj954AvwwZwBgy'
        self.secret_key = '62noVvWuHZpqFKXZyQaEG5lbeg1D1uI19Y8t4Smx'

  
    def upbit_login(self, access_key, secret_key):
        
        
        upbit = pyupbit.exchange_api.Upbit(self.access_key, self.secret_key)
        self.upbit_info = upbit
        
        return self.upbit_info
       
    def account_info(self,upbit_info,uuid,future_prices):    
    
        user_info = self.upbit_info.get_balances()[0]
        print(user_info)
        my_info = user_info[0]
        my_info_price = my_info['balance']
                
        uuid_count = len(self.uuid)
        
        print('='*120)
        print('현재 보유 자산 : ', my_info_price)
        print('전 싸이클 거래 요청 건수 : ', uuid_count)
    
    
    def uncollected(self):
        
        if uuid_count == 0:
            pass
        
        else:
            print('미채결 건수 발생')
            
            for i in self.uuid:
                
                upbit_info.cancel_order(i)
                print('미체결 건수 처리 완료')
                del self.uuid[:] # 주문ID
            

    
        coin_count = len(user_info) - 1  #코인 보유 갯수수
                
    
        for i in range(coin_count):
            coin_info = user_info[i+1] # 보유하고 있는 코인 정보를 1개씩 가져온다.
            
            coin_name = coin_info['currency']
            coin_count = coin_info['balance']
            coin_avg_price = coin_info['avg_buy_price']
            coin_type = coin_info['unit_currency']
            now_price = pyupbit.get_current_price(coin_type + '-' + coin_name)
            orderbook = pyupbit.get_orderbook(coin_type + '-' + coin_name)
            bids_asks = orderbook[0]['orderbook_units']
            down_price = bids_asks[0]['bid_price']
            up_price = bids_asks[0]['ask_price']
            future_yield = coinTool.price_yield(now_price,self.future_prices[i])
            limit_count = coinTool.limit_deal_count(now_price)
            
            self.up_prices.append(up_price)
            self.down_prices.append(down_price)
            self.future_yields.append(future_yield)
            self.now_coin_names.append(coin_type + '-' + coin_name)
            self.now_coin_counts.append(coin_count)
            self.now_avg_buy_prices.append(coin_avg_price)
            self.now_prices.append(now_price)
            self.limit_deal_counts.append(limit_count)
            
        print('현재 보유 코인 개수:',len(self.now_coin_names))
        
    def my_account_data_info(self):
        
        df = [self.now_prices,self.now_coin_counts,self.now_avg_buy_prices,self.future_prices,
              self.future_yields,self.limit_deal_counts,self.up_prices,self.down_prices]
        
        df = np.array(df)
      
        df1 = pd.DataFrame(df,columns = [self.now_coin_names],
                              index = ['now_price','coin_count','avg_buy_prices','future_prices',
                                       'future_yields','limit_count','up_price','down_price']).T
        
        print(df1)
    
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
        
    
    def buy_run(self):
        
        for i,coin in enumerate(self.now_coin_names):
            
            if self.Profit_percent[1] > self.future_yields[i] >= self.Profit_percent[0]:
                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*3)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])
                    
            elif self.Profit_percent[2] > self.future_yields[i] >= self.Profit_percent[1]:
                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*6)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])
                    
            elif self.future_yields[i] >= self.Profit_percent[2]:
                buy_info = self.upbit_info.buy_limit_order(coin,self.down_prices[i],self.limit_deal_counts[i]*9)
                if buy_info[0]['uuid'] == None:
                    pass
                else:
                    self.uuid.append(buy_info[0]['uuid'])



class Selling(Upbit):# 매도
    
    def __init__(self):
        super().__init__()
        
    def sell_run(self):

        for i,count in enumerate(self.now_coin_counts): #C = [z 개수 > 0 ]
            
            if count > 0 :
                sell_coin = self.now_coin_names[i]
                sell_event_yield = coinTool.sell_event_yield(self.now_price[i],self.up_prices[i],self.now_avg_buy_prices[i])
                
                if self.Profit_percent[1]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[0]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_count[i]*(1/6))
                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        
                elif self.Profit_percent[2]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[1]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_count[i]*(2/6))
                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                        
                elif self.Profit_percent[2]*self.AI_modell_accuracy > sell_event_yield >= self.Profit_percent[1]*self.AI_modell_accuracy:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_count[i]*(3/6))
                   
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                
                elif sell_event_yield < self.Profit_percent[2] * 0.25:
                    sell_info = self.upbit_info.sell_limit_order(sell_coin,self.up_prices[i],self.now_coin_count[i])
                    
                    if 'error' in sell_info[0].keys():
                        pass
                    else:
                        self.uuid.append(sell_info[0]['uuid'])
                    
            

# 1분동 15분본 60분봉 으로 각각 예측 정확도를 테스트 실험테스트 하면서 결과를 저장해야된다.           
                


#예측율 업데이트
#예측 평가
#종목 선정
    