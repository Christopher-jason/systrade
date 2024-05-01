import numpy as np
import pandas as pd
import time
import config

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from Orders import Order



def check_cash_balance(client,cost):
    #check if order can be placed
    if client.cash >= cost:
        return True
    else:
        return False


def check_portfolio(client, side):
    portfolio = client.get_open_position()
    #Need to check if postion exist and make trade accordingly
    for postion in portfolio:
        if postion.symbol == 'TSLA' and postion.qty > side:
            print("Don't buy, i guess!!")


tsla_data = pd.read_csv('tsla_live_prices.csv')


def MACD():

    sym = 'TSLA'
    qty = 100
    client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    #Get data
    data = pd.read_csv('tsla_live_prices.csv')
    # Convert to DataFrame for easier manipulation
    closes = data['price'].values
    # Calculate moving averages
    ma10 = np.mean(closes[-300:])  # Last 10 data points
    ma20 = np.mean(closes[-500:])  # Last 20 data points


    print(f"MA100: {ma10}, MA200: {ma20}")



    if ma10 > ma20 and check_cash_balance(client, qty * closes[-1]):  # Check if 10 day MA is above 20 day MA
        print("Buying signal")
        side = OrderSide.BUY
        timeif = TimeInForce.GTC
        o_id = 'Buy_at ' + str(closes[-1])
        buy_order = Order.limit_order(sym,qty,side,timeif,o_id, closes[-1])
        client.submit_order(order_data=buy_order)
        print(buy_order.client_order_id)
    elif ma10 < ma20 :
        print("Selling signal")
        
        side = OrderSide.SELL
        timeif = TimeInForce.GTC
        o_id = 'Sell_at ' + str(ma10)
        sell_order = Order.limit_order(sym,qty,side,timeif,o_id,closes[-1])
        client.submit_order(order_data=sell_order)
        print(sell_order.client_order_id)
        
    


try:
    while True:
        MACD()
        time.sleep(300)  # Correct function call to sleep
except KeyboardInterrupt:
    print("MACD stopped manually")

