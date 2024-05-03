import numpy as np
import pandas as pd
import time
import config

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from Orders import Orders


def MACD():

    order = Orders()

    sym = 'TSLA'
    qty = 100
    client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    #Get data
    data = pd.read_csv('hourly_bars.csv')
    # Convert to DataFrame for easier manipulation
    closes = data['close'].values
    # Calculate moving averages
    ma10 = np.mean(closes[-300:])  # Last 10 data points
    ma20 = np.mean(closes[-500:])  # Last 20 data points

    print(f"MA100: {ma10}, MA200: {ma20}")
    cost = qty * float(closes[-1])

    if ma10 > ma20:  # Check if 10 day MA is above 20 day MA
        print("Buying signal")
        side = OrderSide.BUY
        timeif = TimeInForce.GTC
        o_id = 'Buy_at ' + str(closes[-1])

        if order.check_portfolio(side=side, sym=sym, cost=cost):
            buy_order = Orders.limit_order(sym,qty,side,timeif,o_id, closes[-1])
            client.submit_order(order_data=buy_order)
            print(buy_order.client_order_id)
        


    elif ma10 < ma20 :
        print("Selling signal")
        side = OrderSide.SELL
        timeif = TimeInForce.GTC
        o_id = 'Sell_at ' + str(closes[-1])

        if order.check_portfolio(side=side, sym=sym, cost=cost):
            sell_order = Orders.limit_order(sym,qty,side,timeif,o_id,closes[-1])
            client.submit_order(order_data=sell_order)
            print(sell_order.client_order_id)
        


try:
    while True:
        MACD()
        time.sleep(3600)  # Correct function call to sleep
except KeyboardInterrupt:
    print("MACD stopped manually")

