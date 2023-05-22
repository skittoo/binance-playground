import time
from binance.client import Client

api_key = "your_api_key"
api_secret = "your_api_secret"
client = Client(api_key, api_secret)

def place_order(symbol, quantity, side, ordertype, timeInForce=Client.TIME_IN_FORCE_GTC, price=None):
    try:
        print(f"sending order {side} - {symbol} {quantity} {ordertype} {price}")
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ordertype,
            timeInForce=timeInForce,
            quantity=quantity,
            price=price)
    except Exception as e:
        print("an exception occurred - {}".format(e))
        return False

    return True

def scalp(symbol, quantity):
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    bought = False
    sell_price = 0

    while True:
        new_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        if not bought and new_price < price:
            if place_order(symbol, quantity, Client.SIDE_BUY, Client.ORDER_TYPE_MARKET):
                bought = True
                sell_price = new_price * 1.01  # sell once the price increases by 1%
        elif bought and new_price >= sell_price:
            if place_order(symbol, quantity, Client.SIDE_SELL, Client.ORDER_TYPE_LIMIT, price=sell_price):
                bought = False

        price = new_price
        time.sleep(1)

if __name__ == "__main__":
    scalp("BTCUSDT", "0.001")
