from logic import trading_bot
import logging
import math
from binance.exceptions import BinanceAPIException

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='crypto_bot.log',
                    filemode="a")

quit = ["QUIT", "EXIT"]


def main():
    print("=== Welcome to Binance Futures CLI Bot ===")
    print("Type 'QUIT' or 'EXIT' to exit")
    logging.info("Bot Initialised")

    while True:

        intent = input("What Do you want to do (BUY OR SELL)").strip().upper()

        ## Main Flow
        if intent in quit:
            print("Thanks for using Binance Futures CLI Bot. Goodbye!")
            break

        elif intent == "BUY":

            while True:

                order_type = input(
                    "Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip(
                    ).upper()

                if order_type in quit:
                    print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                    break

                elif order_type == "MARKET":

                    while True:

                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures"
                                )

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)
                                    try:

                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(
                                            f'Mark Price of {symbol}: {mark_price}'
                                        )

                                        notional_value = mark_price * quantity
                                        logging.info(f"Notional Value:{notional_value}")
                                        # min_notional = 20.0 
                                        min_notional = trading_bot.get_min_notional(symbol=symbol)
                                        logging.info(f'Min Notional Value:{min_notional}')  # Binance futures minimum is $20

                                        if notional_value < min_notional:
                                            min_qty_for_notional = min_notional / mark_price
                                            print(f"Order size too small. Minimum notional value is ${min_notional}")

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                trading_bot.place_fututres_order(
                                                    symbol=symbol,
                                                    side=intent,
                                                    quantity=quantity)
                                                print(
                                                    f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                )

                                                logging.info(f"Order Placed")
                                                order_completed = True
                                                break

                                            else:
                                                print(
                                                    f"Insufficient Balance to buy: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )

                                    except BinanceAPIException as e:
                                        print(f'Invalid Quantity:{e}')
                                if order_completed:
                                    break
                    if order_completed:
                        break


                elif order_type == "LIMIT":

                    while True:

                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures"
                                )

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)

                                    try:
                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(
                                            f'Mark Price of {symbol}: {mark_price}'
                                        )
                                        # notional_value = mark_price * quantity
                                        # logging.info(f"Notional Value:{notional_value}")
                                        # # min_notional = 20.0  # Binance futures minimum is $20
                                        # min_notional = trading_bot.get_min_notional(symbol=symbol) 
                                        # logging.info(f'Min Notional Value:{min_notional}') 

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:

                                                while True:

                                                    try:

                                                        price = float(
                                                            input("Price: ").strip())
                                                        logging.info(
                                                            f"Input Price:{price}")
                                                        

                                                        max_price = trading_bot.get_mark_price(
                                                            symbol=symbol)
                                                        logging.info(
                                                            f"Max Price:{max_price}")

                                                        min_price = trading_bot.get_min_price(
                                                            symbol=symbol)
                                                        logging.info(
                                                            f"Min Price: {min_price}")
                                                        
                                                        notional_value = price * quantity
                                                        logging.info(f"Notional Value:{notional_value}")
                                                        # min_notional = 20.0  # Binance futures minimum is $20
                                                        min_notional = trading_bot.get_min_notional(symbol=symbol) 
                                                        logging.info(f'Min Notional Value:{min_notional}') 

                                                        min_required_qty = min_notional / price

                                                        if notional_value < min_notional:
                                                                print(f"Hint: You need at least {min_required_qty:.4f} quantity at this price to meet min notional.")
                                                                raise ValueError(f"Order's notional too small: {notional_value} < {min_notional}")
                                                                                       

                                                        if max_price >= price >= min_price:
                                                            trading_bot.place_futures_limit_order(
                                                                symbol=symbol,
                                                                side=intent,
                                                                quantity=quantity,
                                                                price=price)
                                                            print(
                                                                f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                            )
                                                            logging.info(
                                                                f"Order Placed")
                                                            break
                                                        else:
                                                            print(
                                                                f'Price should be between {min_price}-{max_price}'
                                                            )
                                                    except Exception as e:
                                                        print(f"Invalid Price:{e}")
                                                if order_completed:
                                                    break
                                                # except Exception as e:
                                                #     print(f"Invalid Price:{e}")

                                            else:
                                                print(
                                                    f"Insufficient Balance to BUY: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )
                                    except BinanceAPIException as e:
                                        print(f"Invalid' Quantity:{e}")
                                if order_completed:
                                    break
                    if order_completed:
                        break


                elif order_type == "TWAP":

                    while True:

                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures")
                                

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)

                                    try:

                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(
                                            f'Mark Price of {symbol}: {mark_price}'
                                        )

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            total_quantity = quantity
                                            # while True:
                                            if required_margin < available_margin:
                                                while True:

                                                    try:

                                                        duration_sec = float(input("Duration Sec"). strip())                                                      
                                                    

                                                        if duration_sec > 3:

                                                            try:
                                                                interval_sec = float(
                                                                    input(
                                                                        "Interval Sec"
                                                                    ).strip())

                                                                if duration_sec > interval_sec:

                                                                    num_orders = math.ceil(
                                                                        duration_sec /
                                                                        interval_sec)
                                                                    sub_quantity = total_quantity / num_orders

                                                                    if sub_quantity >= min_qty:

                                                                        trading_bot.place_futures_twap_order(
                                                                            symbol=
                                                                            symbol,
                                                                            side=intent,
                                                                            total_quantity
                                                                            =total_quantity,
                                                                            duration_sec
                                                                            =duration_sec,
                                                                            interval_sec
                                                                            =interval_sec
                                                                        )
                                                                        print(
                                                                            f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                                        )
                                                                        logging.info(
                                                                            f"Order Placed")
                                                                        break
                                                                    else:
                                                                        print(
                                                                            "Try increasing total quantity or reducing interval/duration."
                                                                        )
                                                                    print(
                                                                        "Interval Seconds can not be less than duration seconds"
                                                                    )
                                                                else:
                                                                    print(
                                                                        "Duration Sec can not be less than 3 seconds"
                                                                )
                                                            except Exception as e:
                                                                print(f"Invalid Interval Secs:{e}")
                                                    except Exception as e:
                                                        print(f"Invalid Duration Interval")
                                                        # break
                                            else:
                                                print(
                                                    f"Insufficient Balance to buy TWAP: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )
                                    except BinanceAPIException as e:
                                        print(f"Invalid quantity:{e}")
                                    if order_completed:
                                        break
                    if order_completed:
                        break

                else:
                    print("Invalid Input")

        elif intent == "SELL":
 
            while True:

                order_type = input(
                    "Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip(
                    ).upper()

                if order_type in quit:
                    print("Thanks for using Binance Futures CLI Bot. Goodbye!")
                    break

                elif order_type == "MARKET":

                    while True:


                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures"
                                )

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)
                                    try:
                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(f'Mark Price of {symbol}: {mark_price}')
                                            
                                        

                                        notional_value = mark_price * quantity
                                        logging.info(f"Notional Value:{notional_value}")
                                        # min_notional = 20.0  # Binance futures minimum is $20
                                        min_notional = trading_bot.get_min_notional(symbol=symbol) 
                                        logging.info(f'Min Notional Value:{min_notional}') 

                                        if notional_value < min_notional:
                                            min_qty_for_notional = min_notional / mark_price
                                            print(f"Order size too small. Minimum notional value is ${min_notional}")
                                                
                                            
                                            print(
                                                f"At current price ${mark_price:.2f}, minimum quantity is {min_qty_for_notional:.3f}"
                                            )
                                            continue

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:
                                                trading_bot.place_fututres_order(
                                                    symbol=symbol,
                                                    side=intent,
                                                    quantity=quantity)
                                                print(
                                                    f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                )
                                                logging.info(f"Order Placed")
                                                break
                                            else:
                                                print(
                                                    f"Insufficient Balance to SELL: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )
                                    except BinanceAPIException as e:
                                        print(f'Invalid Quantity:{e}')
                                if order_completed:
                                    break
                    if order_completed:
                        break


                elif order_type == "LIMIT":

                    while True:

                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures"
                                )

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)

                                    try:

                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(
                                            f'Mark Price of {symbol}: {mark_price}'
                                        )

                                        notional_value = mark_price * quantity
                                        logging.info(f"Notional Value:{notional_value}")
                                        # min_notional = 20.0  # Binance futures minimum is $20
                                        min_notional = trading_bot.get_min_notional(symbol=symbol) 
                                        logging.info(f'Min Notional Value:{min_notional}') 

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            if required_margin < available_margin:

                                                while True:

                                                    try:

                                                        price = float( input("Price: ").strip())
                                                    
                                                        logging.info( f"Input Price:{price}")
                                                    

                                                        max_price = trading_bot.get_max_price(
                                                        symbol=symbol)
                                                        logging.info(
                                                        f"Max Price:{max_price}")

                                                        min_price = trading_bot.get_min_price(symbol=symbol)
                                                        
                                                        logging.info(f"Min Price: {min_price}")
                                                        
                                                        notional_value = price * quantity
                                                        logging.info(f"Notional Value:{notional_value}")
                                                        # min_notional = 20.0  # Binance futures minimum is $20
                                                        min_notional = trading_bot.get_min_notional(symbol=symbol) 
                                                        logging.info(f'Min Notional Value:{min_notional}')

                                                        min_required_qty = min_notional / price

                                                        if notional_value < min_notional:
                                                            print(f"Hint: You need at least {min_required_qty:.4f} quantity at this price to meet min notional.")
                                                            raise ValueError(f"Order's notional too small: {notional_value} < {min_notional}")
                                                                

                                                        if not (min_price <= price <=
                                                                max_price):
                                                            print(
                                                                f'Price should be between {min_price}-{max_price}'
                                                            )
                                                            continue

                                                        # if max_price >= price >= min_price:
                                                        trading_bot.place_futures_limit_order(
                                                            symbol=symbol,
                                                            side=intent,
                                                            quantity=quantity,
                                                            price=price)
                                                        print(
                                                            f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                        )
                                                        logging.info(f"Order Placed")
                                                        order_completed = True
                                                        break
                                                    except Exception as e:
                                                        print(f'Invalid Price:{e}')

                                                if order_completed:
                                                    break
                                                # except Exception as e:
                                                #     print(f"Invalid Price:{e}")
                                            # else:
                                            #     print(f'Price should be between {min_price}-{max_price}')

                                            else:
                                                print(
                                                    f"Insufficient Balance to SELL: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )
                                    except BinanceAPIException as e:
                                        print(f'Invalid quantity{e}')
                                if order_completed:
                                    break
                    if order_completed:
                        break


                elif order_type == "TWAP":

                    while True:

                        symbol = input(
                            "Enter symbol (e.g., BTCUSDT): ").strip().upper()

                        if symbol in quit:
                            print(
                                "Thanks for using Binance Futures CLI Bot. Goodbye!"
                            )
                            break

                        else:
                            symbol_exists = trading_bot.symbol_exists(
                                symbol=symbol)

                            logging.info(
                                f"Symbol {symbol} Exists:{symbol_exists}")

                            if symbol_exists == False:
                                print(
                                    f"Symbol {symbol} is not available on Binance Futures"
                                )

                            else:
                                while True:

                                    max_qty = trading_bot.get_max_quantity(
                                        symbol=symbol)

                                    min_qty = trading_bot.get_min_quantity(
                                        symbol=symbol)

                                    try:

                                        quantity = float(
                                            input("Quantity: ").strip())

                                        mark_price = trading_bot.get_mark_price(
                                            symbol=symbol)
                                        logging.info(
                                            f'Mark Price of {symbol}: {mark_price}'
                                        )

                                        required_margin = mark_price * quantity
                                        logging.info(
                                            f'Required Margin:{required_margin}'
                                        )

                                        available_margin = trading_bot.get_available_margin(
                                        )
                                        logging.info(
                                            f'Available Margin:{available_margin}'
                                        )

                                        if max_qty >= quantity >= min_qty:

                                            total_quantity = quantity
                                            # while True:
                                            if required_margin < available_margin:
                                                while True:

                                                    try:

                                                        duration_sec = float(
                                                            input("Duration Sec").
                                                            strip())

                                                        if duration_sec > 3:

                                                            try:
                                                                interval_sec = float(
                                                                    input(
                                                                        "Interval Sec"
                                                                    ).strip())

                                                                if duration_sec > interval_sec:

                                                                    num_orders = math.ceil(
                                                                        duration_sec /
                                                                        interval_sec)
                                                                    sub_quantity = total_quantity / num_orders

                                                                    if sub_quantity >= min_qty:

                                                                        trading_bot.place_futures_twap_order(
                                                                            symbol=
                                                                            symbol,
                                                                            side=intent,
                                                                            total_quantity
                                                                            =total_quantity,
                                                                            duration_sec
                                                                            =duration_sec,
                                                                            interval_sec
                                                                            =interval_sec
                                                                        )
                                                                        print(
                                                                            f"Order Placed of {symbol}: {quantity} for {order_type}"
                                                                        )
                                                                        logging.info( f"Order Placed")
                                                                        
                                                                        
                                                                        break
                                                                    else:
                                                                        print(
                                                                            "Try increasing total quantity or reducing interval/duration."
                                                                        )
                                                            except Exception as e:
                                                                print(f"Invalid Inteval secs:{e}")

                                                            else:
                                                                print(
                                                                    "Interval Seconds can not be less than duration seconds"
                                                                )
                                                        else:
                                                            print(
                                                                "Duration Sec can not be less than 3 seconds")
                                                    
                                                    except Exception as e:
                                                        print(f"Invalid Duration Secs:{e}")
                                                                        
                                            else:
                                                print(
                                                    f"Insufficient Balance to buy TWAP: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
                                                )

                                        else:
                                            print(
                                                f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
                                            )
                                    except BinanceAPIException as e:
                                        print(f"Invalid quantity:{e}")
                                    if order_completed:
                                        break
                    if order_completed:
                            break

        else:
            print("Invalid Input")


if __name__ == "__main__":
    main()



