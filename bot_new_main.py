from bot_main import trading_bot
import logging
import math
from binance.exceptions import BinanceAPIException
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")

quit = ["QUIT", "EXIT"]

def main():
    print("=== Welcome to Binance Futures CLI Bot ===")
    print("Type 'QUIT' or 'EXIT' to exit")
    logging.info("Bot Initialised")

    order_completed = False

    while True:
            
            intent = input("What Do you want to do (BUY OR SELL)").strip().upper()

            ## Main Flow
            if intent in quit:
                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                break

            elif intent == "BUY":

                while True:
  
                    order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()

                    if order_type in quit:
                        print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                        break

                    elif order_type == "MARKET":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                trading_bot.place_fututres_order(symbol=symbol,side=intent,quantity=quantity)
                                                print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                logging.info(f"Order Placed")
                                                order_completed = True
                                                break
                                            else:
                                                print(f"Insufficient Balance to buy: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                            print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")

                    if order_completed == True:
                        break

                    elif order_type == "LIMIT":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                    
                                                    price = float(input("Price: ").strip())
                                                    logging.info(f"Input Price:{price}")

                                                    max_price = trading_bot.get_mark_price(symbol=symbol)
                                                    logging.info(f"Max Price:{max_price}")

                                                    min_price = trading_bot.get_min_price(symbol=symbol)
                                                    logging.info(f"Min Price: {min_price}")

                                                    if max_price >= price >= min_price:
                                                        trading_bot.place_futures_limit_order(symbol=symbol,side=intent,quantity=quantity,price=price)
                                                        print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                        logging.info(f"Order Placed")
                                                        break

                                            else:
                                                print(f"Insufficient Balance to BUY: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                            print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")
    
                        
                    elif order_type == "TWAP":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            total_quantity = quantity
                                            # while True:
                                            if required_margin < available_margin:
                                                while True:

                                                    duration_sec = float(input("Duration Sec").strip())

                                                    if duration_sec > 3:
                                                        interval_sec = float(input("Interval Sec").strip())

                                                        if duration_sec > interval_sec:
                                                            
                                                            num_orders = math.ceil(duration_sec / interval_sec)
                                                            sub_quantity = total_quantity / num_orders

                                                            if sub_quantity >= min_qty:

                                                                trading_bot.place_futures_twap_order(symbol=symbol,side=intent,total_quantity=total_quantity,
                                                                                            duration_sec=duration_sec,interval_sec=interval_sec)
                                                                print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                                logging.info(f"Order Placed")
                                                                break
                                                            else:
                                                                print("Try increasing total quantity or reducing interval/duration.")
                                                            print("Interval Seconds can not be less than duration seconds")
                                                    else:
                                                        print("Duration Sec can not be less than 3 seconds")
                                            else:
                                                print(f"Insufficient Balance to buy TWAP: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                            print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")


                    else:
                         print("Invalid Input")

            elif intent == "SELL":

                while True:

                    order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()

  
                    if order_type in quit:
                        print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                        break

                    elif order_type == "MARKET":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                trading_bot.place_fututres_order(symbol=symbol,side=intent,quantity=quantity)
                                                print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                logging.info(f"Order Placed")
                                                break
                                            else:
                                                print(f"Insufficient Balance to SELL: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                            print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")
                        
                    elif order_type == "LIMIT":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                    
                                                    price = float(input("Price: ").strip())
                                                    logging.info(f"Input Price:{price}")

                                                    max_price = trading_bot.get_mark_price(symbol=symbol)
                                                    logging.info(f"Max Price:{max_price}")

                                                    min_price = trading_bot.get_min_price(symbol=symbol)
                                                    logging.info(f"Min Price: {min_price}")

                                                    if max_price >= price >= min_price:
                                                        trading_bot.place_futures_limit_order(symbol=symbol,side=intent,quantity=quantity,price=price)
                                                        print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                        logging.info(f"Order Placed")
                                                        break

                                            else:
                                                print(f"Insufficient Balance to SELL: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                           print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")


                    elif order_type == "TWAP":

                        while True:
                    
                            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                            if symbol in quit:
                                print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                                break

                            else:
                                symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                                logging.info(f"Symbol {symbol} Exists:{symbol_exists}")

                                if symbol_exists == False:
                                    print(f"Symbol {symbol} is not available on Binance Futures")
                            
                                else:
                                    while True:
                                        
                                        max_qty = trading_bot.get_max_quantity(symbol=symbol)

                                        min_qty = trading_bot.get_min_quantity(symbol=symbol)

                                        quantity = float(input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')

                                        required_margin = mark_price * quantity
                                        logging.info(f'Required Margin:{required_margin}')

                                        available_margin = trading_bot.get_available_margin()
                                        logging.info(f'Available Margin:{available_margin}')

                                        if max_qty >= quantity >= min_qty:

                                            total_quantity = quantity
                                            # while True:
                                            if required_margin < available_margin:
                                                while True:

                                                    duration_sec = float(input("Duration Sec").strip())

                                                    if duration_sec > 3:
                                                        interval_sec = float(input("Interval Sec").strip())

                                                        if duration_sec > interval_sec:
                                                            
                                                            num_orders = math.ceil(duration_sec / interval_sec)
                                                            sub_quantity = total_quantity / num_orders

                                                            if sub_quantity >= min_qty:

                                                                trading_bot.place_futures_twap_order(symbol=symbol,side=intent,total_quantity=total_quantity,
                                                                                            duration_sec=duration_sec,interval_sec=interval_sec)
                                                                print(f"Order Placed of {symbol}: {quantity} for {order_type}" )
                                                                logging.info(f"Order Placed")
                                                                break
                                                            else:
                                                                print("Try increasing total quantity or reducing interval/duration.")

                                                        else:
                                                            print("Interval Seconds can not be less than duration seconds")
                                                    else:
                                                        print("Duration Sec can not be less than 3 seconds")
                                            else:
                                                print(f"Insufficient Balance to buy TWAP: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}")
                                        
                                        else:
                                            print(f"Quantity is not in Range. Range is between {min_qty} - {max_qty}")

                           
            else:
                print("Invalid Input") 

if __name__ == "__main__":
     main()


