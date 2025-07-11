
from bot_main import trading_bot
from binance.exceptions import BinanceAPIException
import logging
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")
quit = ["QUIT", "EXIT"]

# order_placed = False

# while order_placed is False:

#         intent = input("What Do you want to do (BUY OR SELL)").strip().upper()

#         ## Main Flow
#         if intent in quit:
#             print("Thanks for using Binance Futures CLI Bot. Goodbye!")
#             break

#         elif intent == "BUY":

#             while True:

#                 order_type = input(
#                     "Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip(
#                     ).upper()

#                 if order_type in quit:
#                     print("Thanks for using Binance Futures CLI Bot. Goodbye!")
#                     break

#                 elif order_type == "MARKET":

#                     while True:

#                         symbol = input(
#                             "Enter symbol (e.g., BTCUSDT): ").strip().upper()

#                         if symbol in quit:
#                             print(
#                                 "Thanks for using Binance Futures CLI Bot. Goodbye!"
#                             )
#                             break

#                         else:
#                             symbol_exists = trading_bot.symbol_exists(
#                                 symbol=symbol)

#                             logging.info(
#                                 f"Symbol {symbol} Exists:{symbol_exists}")

#                             if symbol_exists == False:
#                                 print(
#                                     f"Symbol {symbol} is not available on Binance Futures"
#                                 )

#                             else:
#                                 while True:

#                                     max_qty = trading_bot.get_max_quantity(
#                                         symbol=symbol)

#                                     min_qty = trading_bot.get_min_quantity(
#                                         symbol=symbol)
#                                     try:

#                                         quantity = float(
#                                             input("Quantity: ").strip())

#                                         mark_price = trading_bot.get_mark_price(
#                                             symbol=symbol)
#                                         logging.info(
#                                             f'Mark Price of {symbol}: {mark_price}'
#                                         )

#                                         required_margin = mark_price * quantity
#                                         logging.info(
#                                             f'Required Margin:{required_margin}'
#                                         )

#                                         available_margin = trading_bot.get_available_margin(
#                                         )
#                                         logging.info(
#                                             f'Available Margin:{available_margin}'
#                                         )

#                                         if max_qty >= quantity >= min_qty:

#                                             if required_margin < available_margin:
#                                                 trading_bot.place_fututres_order(
#                                                     symbol=symbol,
#                                                     side=intent,
#                                                     quantity=quantity)
#                                                 print(
#                                                     f"Order Placed of {symbol}: {quantity} for {order_type}"
#                                                 )

#                                                 logging.info(f"Order Placed")
#                                                 order_placed = True
#                                                 break

#                                             else:
#                                                 print(
#                                                     f"Insufficient Balance to buy: {symbol}.Required Margin is {required_margin} and Available Margin is {available_margin}"
#                                                 )

#                                         else:
#                                             print(
#                                                 f"Quantity is not in Range. Range is between {min_qty} - {max_qty}"
#                                             )

#                                     except BinanceAPIException as e:
#                                         print(f'Invalid Quantity:{e}')
#                 else:
#                     print("Invalid")
        
#         else:
#             print("Invalid")                                # continue

order_placed = False

while not order_placed:

    intent = input("What Do you want to do (BUY OR SELL)").strip().upper()

    ## Main Flow
    if intent in quit:
        print("Thanks for using Binance Futures CLI Bot. Goodbye!")
        break

    elif intent == "BUY":

        while True:

            order_type = input(
                "Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()

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

                        if not symbol_exists:
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

                                        if required_margin < available_margin:
                                            trading_bot.place_fututres_order(
                                                symbol=symbol,
                                                side=intent,
                                                quantity=quantity)
                                            print(
                                                f"Order Placed of {symbol}: {quantity} for {order_type}"
                                            )

                                            logging.info(f"Order Placed")
                                            order_placed = True
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
                            if order_placed:
                                break
                    if order_placed:
                        break
            else:
                print("Invalid")
            if order_placed:
                break
    else:
        print("Invalid")