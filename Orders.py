from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest

class Order:
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
