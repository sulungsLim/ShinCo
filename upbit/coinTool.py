


def price_yield(now_price,future_price):
    
    fees = now_price*0.005
    y = ((future_price - now_price - fees) / now_price) * 100
    
    return round(y,2)



def limit_deal_count(now_price):
    
    limit_count = 501 / now_price
    
    return round(limit_count,3)
    


def sell_event_yield(now_price,up_prices,now_avg_buy_prices): #[(현재가-평균단가-수수료)/현재가*100] 수익률
   
    fees = now_price*0.005
    y = ((up_prices - now_avg_buy_prices - fees) / now_price) * 100
    
    return round(y,2)
        
        