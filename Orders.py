from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide
import config

class Orders:
    client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    def check_cash_balance(self, cost):
        #check if order can be placed
        if self.client.cash >= cost:
            return True
        else:
            return False 
        
    
    def order_decision(self, order_side, position_side, cost, sym ):
        if order_side == OrderSide.BUY and position_side == 'long':
            print("BUY MORE after checking")
            if self.check_cash_balance(cost):
                print("BUY!!")
                return True
            else:
                print("Not enough cash.")
                return False
        elif order_side == OrderSide.BUY and position_side == 'short':
            print("CLOSE position and BUY!!")
            self.client.close_position(sym)
            if self.check_cash_balance(cost):
                print("BUY!!")
                return True
            else:
                print("Not enough cash.")
                return False
        elif order_side == OrderSide.SELL and position_side == 'short':
            print("SELL MORE after checking")
            if self.check_cash_balance(cost):
                print("SELL!!")
                return True
            else:
                print("Not enough buying power?.")
                return False
        elif order_side == OrderSide.SELL and position_side == 'long':
            print("CLOSE position and SELL")
            self.client.close_position(sym)
            if self.check_cash_balance(cost):
                print("SELL!!")
                return True
            else:
                print("Not enough buying power?.")
                return False

    
    def check_portfolio(self, side, sym, cost):
        portfolio = self.client.get_all_positions()
        #Need to check if postion exist and make trade accordingly
        for postion in portfolio:
            if postion.symbol == sym:
                return self.order_decision(side, postion.side, cost, sym)

    



    @staticmethod
    def market_order(symbol, quant, side, time, order_id):
        return MarketOrderRequest(
            symbol = symbol,
            qty = quant,
            side = side,
            time_in_force = time,
            client_order_id = order_id
        )
    
    @staticmethod
    def limit_order(symbol, quant, side, time, order_id, limit_price):
        return LimitOrderRequest(
            symbol = symbol,
            qty = quant,
            side = side,
            time_in_force = time,
            client_order_id = order_id,
            limit_price = limit_price
        )
