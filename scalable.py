# import os
import logging
import json 
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")
from binance import Client
from datetime import datetime
from binance.exceptions import BinanceAPIException, BinanceOrderException

import time
import math

# # api_key = os.getenv('API_KEY')
# # api_secret = os.getenv('SECRET_KEY')

class CryptoBot():

    def __init__(self, api_key, api_secret, testnet=True):
        try:
            self.client = Client(api_key, api_secret,testnet=True)
            logging.info(f"Connection Successful")
        except Exception as e:
            logging.error(f"Error Connecting to Binance: {e}")

    def place_spot_market_order(self, symbol:str, side:str, quantity:float):
        try:
            order = self.client.create_order(
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
        
    def place_futures_limit_order(self,symbol: str, side: str, quantity: float, price: float):
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
            order = self.client.new_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  
            )

            logging.info(f"LIMIT order placed successfully: {order}")

            return order
        
        except Exception as e:
            logging.error(f"Error placing LIMIT order: {e}")
            return None
        
    def validate_symbol(self, symbol):
        """Validate if symbol exists and is tradeable"""
        try:
            exchange_info = self.client.futures_exchange_info()
            symbols = [s['symbol'] for s in exchange_info['symbols'] if s['status'] == 'TRADING']
            
            if symbol not in symbols:
                logging.error(f"Invalid symbol: {symbol}")
                return False
            
            logging.info(f"Symbol {symbol} validated successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error validating symbol: {e}")
            return False


    def place_futures_twap_order(self,symbol, side, total_quantity, duration_sec, interval_sec):
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

            logging.info(f"Placing TWAP order: {num_orders} x {sub_quantity} {symbol} {side} every {interval_sec} sec")

            for i in range(num_orders):
                print(f"Placing part {i+1}/{num_orders}...")
                # Here you use your market order function:
                self.place_spot_market_order(symbol, side, sub_quantity)
                
                if i < num_orders - 1:
                    time.sleep(interval_sec)

            logging.info("TWAP execution completed.")

        except Exception as e:
            logging.error(f"Error in TWAP execution: {e}")




bot = CryptoBot(api_key=api_key,api_secret=api_secret,testnet=True)


# class BasicBot:


#     def __init__(self, api_key, api_secret, testnet=True):
#         """
#         Initialize the trading bot with Binance API credentials
        
#         Args:
#             api_key (str): Binance API key
#             api_secret (str): Binance API secret
#             testnet (bool): Use testnet environment
#         """
#         try:
#             self.client = Client(api_key, api_secret, testnet=testnet)
            
#             # Test connection
#             self.client.ping()
#             logging.info(f"Successfully connected to Binance API (testnet={testnet})")
            
#             # Get account info to verify futures trading is enabled
#             account_info = self.client.futures_account()
#             logging.info(f"Account balance: {account_info['totalWalletBalance']} USDT")
            
#         except Exception as e:
#             logging.error(f"Failed to initialize bot: {e}")
#             raise

#     def validate_symbol(self, symbol):
#         """Validate if symbol exists and is tradeable"""
#         try:
#             exchange_info = self.client.futures_exchange_info()
#             symbols = [s['symbol'] for s in exchange_info['symbols'] if s['status'] == 'TRADING']
            
#             if symbol not in symbols:
#                 logging.error(f"Invalid symbol: {symbol}")
#                 return False
            
#             logging.info(f"Symbol {symbol} validated successfully")
#             return True
            
#         except Exception as e:
#             logging.error(f"Error validating symbol: {e}")
#             return False

#     def get_symbol_info(self, symbol):
#         """Get symbol information including price filters"""
#         try:
#             exchange_info = self.client.futures_exchange_info()
#             for s in exchange_info['symbols']:
#                 if s['symbol'] == symbol:
#                     return s
#             return None
#         except Exception as e:
#             logging.error(f"Error getting symbol info: {e}")
#             return None

#     def place_futures_market_order(self, symbol, side, quantity):
#         """
#         Place a market order on Binance Futures
        
#         Args:
#             symbol (str): Trading pair (e.g., 'BTCUSDT')
#             side (str): 'BUY' or 'SELL'
#             quantity (float): Order quantity
            
#         Returns:
#             dict: Order response
#         """
#         try:
#             logging.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            
#             # Log API request
#             request_data = {
#                 'symbol': symbol,
#                 'side': side,
#                 'type': 'MARKET',
#                 'quantity': quantity
#             }
#             logging.info(f"API Request: {json.dumps(request_data, indent=2)}")
            
#             # Place order
#             order = self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type=Client.ORDER_TYPE_MARKET,
#                 quantity=quantity
#             )
            
#             # Log API response
#             logging.info(f"API Response: {json.dumps(order, indent=2)}")
            
#             return {
#                 'status': 'SUCCESS',
#                 'order_id': order['orderId'],
#                 'symbol': order['symbol'],
#                 'side': order['side'],
#                 'type': order['type'],
#                 'quantity': order['origQty'],
#                 'price': order.get('price', 'MARKET'),
#                 'fills': order.get('fills', []),
#                 'timestamp': datetime.now().isoformat()
#             }
            
#         except BinanceAPIException as e:
#             error_msg = f"Binance API Error: {e.message}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}
            
#         except BinanceOrderException as e:
#             error_msg = f"Binance Order Error: {e.message}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}
            
#         except Exception as e:
#             error_msg = f"Unexpected error: {str(e)}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}

#     def place_futures_limit_order(self, symbol, side, quantity, price):
#         """
#         Place a limit order on Binance Futures
        
#         Args:
#             symbol (str): Trading pair (e.g., 'BTCUSDT')
#             side (str): 'BUY' or 'SELL'
#             quantity (float): Order quantity
#             price (float): Limit price
            
#         Returns:
#             dict: Order response
#         """
#         try:
#             logging.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
            
#             # Log API request
#             request_data = {
#                 'symbol': symbol,
#                 'side': side,
#                 'type': 'LIMIT',
#                 'quantity': quantity,
#                 'price': price,
#                 'timeInForce': 'GTC'
#             }
#             logging.info(f"API Request: {json.dumps(request_data, indent=2)}")
            
#             # Place order
#             order = self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type=Client.ORDER_TYPE_LIMIT,
#                 quantity=quantity,
#                 price=price,
#                 timeInForce=Client.TIME_IN_FORCE_GTC
#             )
            
#             # Log API response
#             logging.info(f"API Response: {json.dumps(order, indent=2)}")
            
#             return {
#                 'status': 'SUCCESS',
#                 'order_id': order['orderId'],
#                 'symbol': order['symbol'],
#                 'side': order['side'],
#                 'type': order['type'],
#                 'quantity': order['origQty'],
#                 'price': order['price'],
#                 'timestamp': datetime.now().isoformat()
#             }
            
#         except BinanceAPIException as e:
#             error_msg = f"Binance API Error: {e.message}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}
            
#         except BinanceOrderException as e:
#             error_msg = f"Binance Order Error: {e.message}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}
            
#         except Exception as e:
#             error_msg = f"Unexpected error: {str(e)}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}

#     def place_futures_twap_order(self, symbol, side, quantity, duration, interval):
#         """
#         Place a TWAP (Time-Weighted Average Price) order
#         Splits the order into smaller chunks over time
        
#         Args:
#             symbol (str): Trading pair
#             side (str): 'BUY' or 'SELL'
#             quantity (float): Total quantity
#             duration (int): Total duration in seconds
#             interval (int): Interval between orders in seconds
            
#         Returns:
#             dict: TWAP execution summary
#         """
#         try:
#             logging.info(f"Starting TWAP order: {side} {quantity} {symbol} over {duration}s with {interval}s intervals")
            
#             # Calculate number of orders and quantity per order
#             num_orders = max(1, duration // interval)
#             quantity_per_order = quantity / num_orders
            
#             orders = []
#             total_filled = 0
            
#             for i in range(num_orders):
#                 try:
#                     # Place market order for this chunk
#                     order_response = self.place_futures_market_order(symbol, side, quantity_per_order)
                    
#                     if order_response['status'] == 'SUCCESS':
#                         orders.append(order_response)
#                         total_filled += float(order_response['quantity'])
#                         logging.info(f"TWAP chunk {i+1}/{num_orders} executed successfully")
#                     else:
#                         logging.error(f"TWAP chunk {i+1}/{num_orders} failed: {order_response.get('error', 'Unknown error')}")
                    
#                     # Wait for next interval (except for last order)
#                     if i < num_orders - 1:
#                         time.sleep(interval)
                        
#                 except Exception as e:
#                     logging.error(f"Error in TWAP chunk {i+1}: {e}")
#                     continue
            
#             return {
#                 'status': 'SUCCESS',
#                 'strategy': 'TWAP',
#                 'symbol': symbol,
#                 'side': side,
#                 'total_quantity': quantity,
#                 'filled_quantity': total_filled,
#                 'num_orders': len(orders),
#                 'orders': orders,
#                 'timestamp': datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             error_msg = f"TWAP execution error: {str(e)}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}

#     def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
#         """
#         Place a stop-limit order (Advanced order type)
        
#         Args:
#             symbol (str): Trading pair
#             side (str): 'BUY' or 'SELL'
#             quantity (float): Order quantity
#             stop_price (float): Stop price
#             limit_price (float): Limit price
            
#         Returns:
#             dict: Order response
#         """
#         try:
#             logging.info(f"Placing STOP_LIMIT order: {side} {quantity} {symbol} @ stop:{stop_price} limit:{limit_price}")
            
#             request_data = {
#                 'symbol': symbol,
#                 'side': side,
#                 'type': 'STOP',
#                 'quantity': quantity,
#                 'stopPrice': stop_price,
#                 'price': limit_price,
#                 'timeInForce': 'GTC'
#             }
#             logging.info(f"API Request: {json.dumps(request_data, indent=2)}")
            
#             order = self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type='STOP',
#                 quantity=quantity,
#                 stopPrice=stop_price,
#                 price=limit_price,
#                 timeInForce=Client.TIME_IN_FORCE_GTC
#             )
            
#             logging.info(f"API Response: {json.dumps(order, indent=2)}")
            
#             return {
#                 'status': 'SUCCESS',
#                 'order_id': order['orderId'],
#                 'symbol': order['symbol'],
#                 'side': order['side'],
#                 'type': order['type'],
#                 'quantity': order['origQty'],
#                 'stop_price': stop_price,
#                 'limit_price': limit_price,
#                 'timestamp': datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             error_msg = f"Stop-limit order error: {str(e)}"
#             logging.error(error_msg)
#             return {'status': 'ERROR', 'error': error_msg}

#     def get_account_balance(self):
#         """Get account balance"""
#         try:
#             account = self.client.futures_account()
#             return {
#                 'total_balance': account['totalWalletBalance'],
#                 'available_balance': account['availableBalance'],
#                 'assets': account['assets']
#             }
#         except Exception as e:
#             logging.error(f"Error getting account balance: {e}")
#             return None

#     def get_open_orders(self, symbol=None):
#         """Get open orders"""
#         try:
#             orders = self.client.futures_get_open_orders(symbol=symbol)
#             return orders
#         except Exception as e:
#             logging.error(f"Error getting open orders: {e}")
#             return []