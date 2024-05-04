import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST
from alpaca_trade_api.entity import Position, Account
from alpaca_trade_api.common import URL
import config

class Orders:
    def __init__(self):
        self.client = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url='https://paper-api.alpaca.markets/v2')

    def check_cash_balance(self, cost):
        account = self.client.get_account()
        cash = float(account.buying_power)
        return cash >= cost

    def order_decision(self, order_side, position_side, cost, sym):
        if order_side == 'buy' and position_side == 'long':
            print("BUY MORE after checking")
            if self.check_cash_balance(cost):
                print("BUY!!")
                return True
            else:
                print("Not enough cash.")
                return False
        elif order_side == 'buy' and position_side == 'short':
            self.client.close_position(sym)
            if self.check_cash_balance(cost):
                print("CLOSE position and BUY!!")
                return True
            else:
                print("Not enough cash.")
                return False
        elif order_side == 'sell' and position_side == 'short':
            if self.check_cash_balance(cost):
                print("SELL MORE after checking")
                print("SELL!!")
                return True
            else:
                print("Not enough buying power.")
                return False
        elif order_side == 'sell' and position_side == 'long':
            self.client.close_position(sym)
            if self.check_cash_balance(cost):
                print("CLOSE position and SELL")
                return True
            else:
                print("Not enough buying power.")
                return False



    def check_portfolio(self, side, sym, cost):
        portfolio = self.client.list_positions()
        for position in portfolio:
            if position.symbol == sym:
                return self.order_decision(side, position.side, cost, sym)

    @staticmethod
    def market_order(client, symbol, qty, side, time_in_force, client_order_id):
        return client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force=time_in_force,
            client_order_id=client_order_id
        )

    @staticmethod
    def limit_order(client, symbol, qty, side, time_in_force, order_id, limit_price):
        return client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            time_in_force=time_in_force,
            client_order_id=order_id,
            limit_price=limit_price
        )

# Example Usage
orders = Orders()
print(orders.check_cash_balance(1000))
# Usage of static method needs a client instance
client = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url='https://paper-api.alpaca.markets')
Orders.market_order(client, 'AAPL', 10, 'buy', 'gtc', 'my_order_id_123')
