import coin
import pyupbit
#import upbit_Auto as uA
import coin_1

class Coin_name_info:
    
    def __init__(self):
        
        self.base_coin_name = ['KRW-KNC','KRW-COSM','KRW-POWR','KRW-XRP']
        self.now_coin_names_inquiry = []
        self.login_key()        
        self.coin_name_inquiry()
        
        
    def login_key(self):
           
        self.access_key = 'jlY7Psx9dJHRSsHE0rO8HGllu8cj954AvwwZwBgy'
        self.secret_key = '62noVvWuHZpqFKXZyQaEG5lbeg1D1uI19Y8t4Smx'


    def coin_name_inquiry(self):
        
        upbit = pyupbit.exchange_api.Upbit(self.access_key, self.secret_key)
        user_info = upbit.get_balances()[0]
        
        coin_num = len(user_info) - 1
        
        
        for i in range(coin_num):
            
            coin_info = user_info[i+1]
            coin_type = coin_info['unit_currency']
            coin_name = coin_info['currency']
            
            self.now_coin_names_inquiry.append(coin_type + '-' + coin_name)
            
        #print(self.now_coin_names_inquiry)  

class Prediction(Coin_name_info):
    
    def __init__(self):
        super().__init__()
         
        self.f_price = []
        self.winner_coins = []
        self.scoerer = []
        self.futuer_prices = []
        self.future_price_LSTM = []
        self.df = []
        
        
        
        self.base_df = []
        self.base_futuer_prices = []
        self.base_future_price_LSTM = []
        
        self.data_inquiry()
        
        self.futuer_price()
        
        
    def data_inquiry(self):

        for i in self.now_coin_names_inquiry:
            
            self.df.append(pyupbit.get_ohlcv(i, interval="minute15",count=100).loc[::-1].reset_index().rename(columns={'index':'date'}))
            
        
        for i in self.base_coin_name:
            
             self.base_df.append(pyupbit.get_ohlcv(i, interval="minute15",count=100).loc[::-1].reset_index().rename(columns={'index':'date'}))

            
            

    
    def add_culumns(self):
        
        for i in self.now_coin_names_inquiry:
            
            self.coin_data_i = coin.Indicators(self.coin_name_i)       
            
        
    def accuracy_evaluation(self):
        
       for i in self.now_coin_names_inquiry:
           
           self.f_price_i.append(coin.predcoin(self.coin_data_i))
           
    def winner_coin(self):
        
        for i in self.now_coin_names_inquiry:
           
           self.winner_coin_i.append(coin.predcoin(self.coin_data_i))
           
    
    def futuer_price(self):
        
        #UAA = accuracy.Prediction()
        #a = self.now_coin_names_inquiry
        self.coin_names = [i[4:] for i in  self.now_coin_names_inquiry]
        self.base_coin_names = [i[4:] for i in  self.base_coin_name]
        
        for i in range(len(self.coin_names)):
            
            val = coin_1.predcoin(self.coin_names[i],self.df[i])
            
            for j in range(len(val)):
                if j==0:
                    val[j]=round(val[j][0][0],2)
                else:
                    val[j]=round(val[j][0],2)
                    
            self.futuer_prices.append(val)
        
        for i in self.futuer_prices:
            
            self.future_price_LSTM.append(i[0])
            
        ############################################################
        for i in range(len(self.base_coin_names)):
            
            val = coin_1.predcoin(self.base_coin_names[i],self.base_df[i])
            
            for j in range(len(val)):
                if j==0:
                    val[j]=round(val[j][0][0],2)
                else:
                    val[j]=round(val[j][0],2)
                    
            self.base_futuer_prices.append(val)
        
        for i in self.base_futuer_prices:
            
            self.base_future_price_LSTM.append(i[0])
            
        
     
        
