import coin
import pyupbit
import pandas as pd
import numpy as np
import upbit_Auto as ua

class data_maker():
    
    def __init__(self):
        
        self.coin_name = ua.Upbit.now_coin_names
        self.f_price = []
        self.winner_coins = []
        self.scoerer = []
        
     
    def data_inquiry(self):

        for i in self.coin_name:

            self.coin_name_i = pyupbit.get_ohlcv(i, interval="minute15").loc[::-1].reset_index().rename(columns={'index':'date'})
            #self.coin_name(KRW-ETH ),self.coin_name(KRW-XRP),self.coin_name(KRW-POWR ),self.coin_name(KRW-KNC)
        
        self.coin_num = len(self.coin_name)

        
    
    def add_culumns(self):
        
        for i in self.coin_name:
            
            self.coin_data_i = coin.Indicators(self.coin_name_i)       
            
        
    def accuracy_evaluation(self):
        
       for i in self.coin_name:
           
           self.f_price.append(coin.predcoin(self.coin_data_i))
           
    def winner_coin(self):
        
        for i in self.coin_name:
           
           self.winner_coin.append(coin.predcoin(self.coin_data_i))
        
        
        
    def scoer(self):
        
        a = []
        
        for i in self.result:
            
            if i > 80:
                a.append(1)
            else:
                a.append(0)
                
        self.score.append(sum(a))
        
           

          
           
#%%
           
        
