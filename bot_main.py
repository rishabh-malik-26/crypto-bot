from binance.client import Client
import logging
import time
from datetime import datetime
import math
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = "d4ea544c086db181db7f66e1b108f0da624b4a9b59c2fdefb610e64775ebdc06"
SECRET_KEY = "238a456593a6a5b52fcf38ff6b0fc8f5c8fcd7bca4c938c71f63162d0f874f54"

class Bot():
    def __init__(self, api_key, api_secret, testnet = True):
        try:
            self.client = Client(api_key, api_secret)
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

            logging.info(f"Connection Successful")
        except Exception as e:
            logging.error(f"Connection Failed")

    def place_fututres_order(self, symbol:str, side:str, quantity:float):

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),  
                type='MARKET',
                quantity=quantity
            )
            logging.info(f"Future Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Future Order Failed:{e}")
            raise



    def place_futures_limit_order(self,symbol: str, side: str,quantity: float, price: float):
            if side.upper() not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'.")

            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            if price <= 0:
                raise ValueError("Price must be greater than 0.")

            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce='GTC'          # "Good Till Cancelled" – required for LIMIT orders

            )

            logging.info(f"LIMIT order placed successfully: {order}")
            return order


    def get_symbol_filters(self, symbol: str):
        """Get the filters for a  symbol from exchange info."""
        try:
            info = self.client.futures_exchange_info()
            symbol_info = next((s for s in info['symbols'] if s['symbol'] == symbol.upper()), None)
            if not symbol_info:
                raise ValueError(f"Symbol {symbol} not found in exchange info.")
            filters = {f['filterType']: f for f in symbol_info['filters']}
            return filters
        except Exception as e:
            logging.error(f"Failed to fetch filters for {symbol}: {str(e)}")
            raise

    def get_min_quantity(self, symbol: str) -> float:
        """
        Returns the minimum quantity allowed for the given Futures symbol.
        """
        try:
            info = self.client.futures_exchange_info()
            symbol_info = next((s for s in info['symbols'] if s['symbol'] == symbol.upper()), None)
            if not symbol_info:
                raise ValueError(f"Symbol '{symbol}' not found.")

            lot_filter = next(f for f in symbol_info['filters'] if f['filterType'] == "LOT_SIZE")
            return float(lot_filter["minQty"])
        except Exception as e:
            logging.error(f"Error fetching min quantity for {symbol}: {e}")
            raise
        
    def get_max_quantity(self, symbol: str) -> float:
        """
        Returns the maximum quantity allowed for the given Futures symbol.
        """
        try:
            info = self.client.futures_exchange_info()
            symbol_info = next((s for s in info['symbols'] if s['symbol'] == symbol.upper()), None)
            if not symbol_info:
                raise ValueError(f"Symbol '{symbol}' not found.")

            lot_filter = next(f for f in symbol_info['filters'] if f['filterType'] == "LOT_SIZE")
            return float(lot_filter["maxQty"])
        except Exception as e:
            logging.error(f"Error fetching max quantity for {symbol}: {e}")
            raise


    def place_futures_twap_order(self, symbol, side, total_quantity, duration_sec, interval_sec):
        try:
            if duration_sec < interval_sec:
                raise ValueError("Duration must be greater than interval.")

            num_orders = math.ceil(duration_sec / interval_sec)
            sub_quantity = total_quantity / num_orders

            sub_quantity = round(sub_quantity, 3)

            logging.info(f"Placing TWAP order: {num_orders} x {sub_quantity} {symbol} {side} every {interval_sec} sec")

            for i in range(num_orders):
                logging.info(f"Placing part {i+1}/{num_orders} at {datetime.now().strftime('%H:%M:%S')}...")
                self.place_fututres_order(symbol, side, sub_quantity)

                if i < num_orders - 1:
                    time.sleep(interval_sec)

            logging.info("TWAP execution completed.")

        except Exception as e:
            logging.error(f"Error in TWAP execution: {e}")
            raise

    def symbol_exists(self, symbol: str) -> bool:
        """
        Check if the symbol exists in Binance Futures exchange info.
        Returns True if valid, False otherwise.
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    return True
            return False
        except Exception as e:
            logging.error(f"Error checking symbol {symbol}: {str(e)}")
        return False
    
    def get_futures_balance(self, asset="USDT"):
        """
        Returns the available balance of a given asset (default: USDT) in the Futures wallet.
        """
        try:
            balances = self.client.futures_account_balance()
            for entry in balances:
                if entry["asset"] == asset.upper():
                    available = float(entry["balance"])
                    logging.info(f"Available {asset} Balance: {available}")
                    return available
            raise ValueError(f"{asset} balance not found.")
        except Exception as e:
            logging.error(f"Error fetching futures balance: {e}")
            raise


    def get_mark_price(self, symbol: str) -> float:
        try:
            price_data = self.client.futures_mark_price(symbol=symbol)
            return float(price_data["markPrice"])
        except Exception as e:
            logging.error(f"Error fetching mark price for {symbol}: {e}")
            raise
        
    def get_available_margin(self) -> float:
        try:
            account_info = self.client.futures_account()
            return float(account_info["availableBalance"])
        except Exception as e:
            logging.error(f"Error fetching available margin: {e}")
            raise

    def estimate_required_margin(self, symbol: str, quantity: float, leverage: int) -> float:
        try:
            price = self.get_mark_price(symbol)
            cost = (price * quantity) / leverage
            return cost
        except Exception as e:
            logging.error(f"Error estimating required margin: {e}")
            raise


    def get_min_price(self, symbol: str) -> float:
        """
        Returns the minimum allowed price (minPrice) for the given futures symbol.
        """
        try:
            info = self.client.futures_exchange_info()
            symbol_info = next(s for s in info["symbols"] if s["symbol"] == symbol.upper())
            price_filter = next(f for f in symbol_info["filters"] if f["filterType"] == "PRICE_FILTER")
            return float(price_filter["minPrice"])
        except Exception as e:
            logging.error(f"Error fetching min price for {symbol}: {e}")
            raise



trading_bot = Bot(api_key=API_KEY,api_secret=SECRET_KEY)


# data  = trading_bot.get_max_qty("BTCUSDT")

# print(data['filters'])
# # trading_bot.place_fututres_order(symbol="BTCUSDT",side="BUY",quantity=0.4)

# print(trading_bot.get_symbol_filters(symbol="BTCUSDT"))


