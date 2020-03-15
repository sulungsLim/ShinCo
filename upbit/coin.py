import os
import pandas as pd
import numpy as np
import talib
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler,RobustScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib 
from keras.models import load_model
import lightgbm as lgb
import xgboost

class NN():
    
    def __init__(self):
        
        self.xs = joblib.load('Xscale.pkl')
        self.ys = joblib.load('Yscale.pkl')
        self.LSTM = load_model('LSTM.h5')
        
        
        self.lgb1 = joblib.load('lgb.pkl')
        self.lgb2 = joblib.load('lgb2.pkl')
        self.xgb = joblib.load('xgb.pkl')
        
        self.result = []
        
        

    def Indicators(self,df): # date close open high low volume 컬럼순 
                        # 결측치 33줄 생김 0~32 까지
        df['sma5'] = talib.SMA(np.asarray(df['close']), 5)
        df['sma20'] = talib.SMA(np.asarray(df['close']), 20)
        #df['sma120'] = talib.SMA(np.asarray(df['close']), 120)
        df['ema12'] = talib.SMA(np.asarray(df['close']), 12)
        df['ema26'] = talib.SMA(np.asarray(df['close']), 26)
        upper, middle, lower = talib.BBANDS(np.asarray(df['close']), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        df['dn'] = lower
        df['mavg'] = middle
        df['up'] = upper
        df['pctB'] = (df.close - df.dn)/(df.up - df.dn)
        rsi14 = talib.RSI(np.asarray(df['close']), 14)
        df['rsi14'] = rsi14
        macd, macdsignal, macdhist = talib.MACD(np.asarray(df['close']), 12, 26, 9)  
        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['obv']=talib.OBV(df['close'], df['volume'])
        df['ad'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])
        df['ADOSC'] = talib.ADOSC(df['high'], df['low'], df['close'], df['volume'], fastperiod=3, slowperiod=10)
        df=df.iloc[33:]
        df=df.fillna(0)
        df=df.drop(columns=['date'])
        
        self.add_columns_data = df


    def predcoin(self):

        df = self.add_columns_data
        
        nptf = np.array(df[-50:])
        nptf = pd.DataFrame(self.xs.transform(nptf), columns = df.columns)
        nptf = np.array(nptf)
        nptf = nptf.reshape(1,50,-1)
        
        self.result.append(self.ys.inverse_transform(self.LSTM.predict(nptf)))
        
        nptf=np.array(df.iloc[-1])
        nptf=nptf.reshape(1,-1)
        
        self.result.append(self.lgb1.predict(nptf))
        self.result.append(self.lgb2.predict(nptf))
        self.result.append(self.xgb.predict(nptf))
        
    
    def winner_coin(self):
        
        a=[]
        for i in self.result:
            if i > 80:
                a.append(1)
            else:
                a.append(0)
                
        self.score.append(sum(a))

        
