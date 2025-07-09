import os
from binance import Client
import logging
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")

api_key = "rBQVkQTyZ6hbAnG6LuimaIPERY9ToOpsPHwLXtR8IGaKLYVnS66eoZW8BEYjwKhW"
api_secret = "jEC53VXZj3oOV7W3sAzLuGnvkME2Oq0NZxVPCiTUXKcf1xz1z6XdbYhsdQrOicC0"

client = Client(api_key, api_secret, testnet=True)

def place_spot_market_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,   # "BUY" or "SELL"
            type='MARKET',
            quantity=quantity
        )
        logging.info(f"Spot Market Order placed: {order}")
        return order
    except Exception as e:
        logging.error(f"Error placing Spot Market Order: {e}")
        raise

def place_futures_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Place a LIMIT order on USDT-M Futures Testnet.

    Args:
        symbol (str): e.g., 'BTCUSDT'
        side (str): 'BUY' or 'SELL'
        quantity (float): e.g., 0.001
        price (float): limit price

    Returns:
        dict: API response with order details
    """
    try:
        # Validate side
        if side.upper() not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'.")

        # Validate inputs
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        # Create limit order
        order = client.new_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'  # Good-Til-Cancelled is required for LIMIT orders
        )

        logging.info(f"LIMIT order placed successfully: {order}")
        print(f"LIMIT order placed successfully: {order}")

        return order

    except Exception as e:
        logging.error(f"Error placing LIMIT order: {e}")
        print(f"Error placing LIMIT order: {e}")
        return None



import time
import math

def place_futures_twap_order(symbol, side, total_quantity, duration_sec, interval_sec):
    """
    Place a TWAP order by splitting total quantity into equal parts.

    Args:
        symbol (str): e.g., 'BTCUSDT'
        side (str): 'BUY' or 'SELL'
        total_quantity (float): Total quantity to trade
        duration_sec (int): Total duration in seconds to execute the TWAP
        interval_sec (int): Interval between each sub-order in seconds
    """
    try:
        # Calculate number of sub-orders
        num_orders = math.ceil(duration_sec / interval_sec)
        sub_quantity = total_quantity / num_orders

        print(f"Placing TWAP order: {num_orders} x {sub_quantity} {symbol} {side} every {interval_sec} sec")

        for i in range(num_orders):
            print(f"Placing part {i+1}/{num_orders}...")
            # Here you use your market order function:
            place_spot_market_order(symbol, side, sub_quantity)
            
            if i < num_orders - 1:
                time.sleep(interval_sec)

        print("TWAP execution completed.")

    except Exception as e:
        logging.error(f"Error in TWAP execution: {e}")
        print(f"Error in TWAP: {e}")

# place_spot_market_order(symbol= "BTCUSDT" ,side="BUY" ,quantity=0.01)

# place_futures_limit_order(symbol="BTCUSDT",side="BUY",quantity=0.1,price=1223)