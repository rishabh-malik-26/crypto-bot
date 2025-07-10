from bot_main import trading_bot
import logging
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")
from utils import get_valid_input

def main():
    print("=== Welcome to Binance Futures CLI Bot ===")
    logging.info("Bot Initialised")

    try:

            intent = input("What Do you want to do (BUY OR SELL)").strip().upper()

            if intent == "BUY":

                order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
                logging.info(f"Order type Selected:{order_type}")

                if order_type == "MARKET":

                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()

                    symbol_exists = trading_bot.symbol_exists(symbol=symbol)

                    logging.info(f"Symbol {symbol} Existes:{symbol_exists}")

                    if not trading_bot.symbol_exists(symbol):
                        print(f"Symbol '{symbol}' is not available on Binance Futures.")


                    quantity = float(input("Quantity: ").strip())

                    if quantity >= 0:
                        logging.info(f"Quantity:{quantity}")

                        trading_bot.place_fututres_order(symbol=symbol,side=intent,quantity=quantity)

                    else:
                        logging.info(f"Quantity:{quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")
            
                elif order_type == "LIMIT":
                
                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                    trading_bot.get_symbol_filters(symbol=symbol)
                    logging.info(f'Symbol Input {symbol}')

                    quantity = float(input("Quantity: ").strip())

                    if quantity >= 0:
                        logging.info(f"Quantity:{quantity}")

                        price = float(input("Price: ").strip())

                        if price > 0:
                            trading_bot.place_futures_limit_order(symbol=symbol,side=intent,quantity=quantity,price=price)
                        else:
                            logging.info(f'Price input is 0 or negative')
                            raise ValueError(f"Quantity can not be equal of less that 0")

                    else:
                        logging.info(f"Quantity:{quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")

                elif order_type == "TWAP":

                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                    trading_bot.get_symbol_filters(symbol=symbol)
                    logging.info(f'Symbol Input {symbol}')

                    total_quantity = float(input("Quantity: ").strip())

                    if total_quantity >= 0:
                        logging.info(f"Quantity:{total_quantity}")

                        duration_sec = float(input("Duration Seconds: ").strip())

                        if duration_sec > 0:

                            interval_sec =  float(input("Interval Seconds: ").strip())
                            if   interval_sec > 0:    
                                trading_bot.place_futures_twap_order(symbol=symbol,side=intent,total_quantity=total_quantity,duration_sec=duration_sec,interval_sec=interval_sec)
                        else:
                            logging.info(f'duration_sec input is 0 or negative')
                            raise ValueError(f"duration_sec can not be equal of less that 0")

                    else:
                        logging.info(f"Quantity:{total_quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")

            elif intent == "SELL":
                order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
                logging.info(f"Order type Selected:{order_type}")

                if order_type == "MARKET":

                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                    trading_bot.get_symbol_filters(symbol=symbol)
                    logging.info(f'Symbol Input {symbol}')

                    quantity = float(input("Quantity: ").strip())

                    if quantity >= 0:
                        logging.info(f"Quantity:{quantity}")

                        trading_bot.place_fututres_order(symbol=symbol,side=intent,quantity=quantity)

                    else:
                        logging.info(f"Quantity:{quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")
            
                elif order_type == "LIMIT":
                
                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                    trading_bot.get_symbol_filters(symbol=symbol)
                    logging.info(f'Symbol Input {symbol}')

                    quantity = float(input("Quantity: ").strip())

                    if quantity >= 0:
                        logging.info(f"Quantity:{quantity}")

                        price = float(input("Price: ").strip())

                        if price > 0:
                            trading_bot.place_futures_limit_order(symbol=symbol,side=intent,quantity=quantity,price=price)
                        else:
                            logging.info(f'Price input is 0 or negative')
                            raise ValueError(f"Quantity can not be equal of less that 0")

                    else:
                        logging.info(f"Quantity:{quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")

                elif order_type == "TWAP":

                    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                    trading_bot.get_symbol_filters(symbol=symbol)
                    logging.info(f'Symbol Input {symbol}')

                    total_quantity = float(input("Quantity: ").strip())

                    if total_quantity >= 0:
                        logging.info(f"Quantity:{total_quantity}")

                        duration_sec = float(input("Duration Seconds: ").strip())

                        if duration_sec > 0:

                            interval_sec =  float(input("Interval Seconds: ").strip())
                            if   interval_sec > 0:    
                                trading_bot.place_futures_twap_order(symbol=symbol,side=intent,total_quantity=total_quantity,duration_sec=duration_sec,interval_sec=interval_sec)
                        else:
                            logging.info(f'duration_sec input is 0 or negative')
                            raise ValueError(f"duration_sec can not be equal of less that 0")

                    else:
                        logging.info(f"Quantity:{total_quantity}")
                        raise ValueError(f"Quantity can not be equal of less that 0")

            else:
                logging.error(f"Invalid Input: {intent}")
                raise ValueError(f"Invalid Input")

    except Exception as e:
        return e 
                # order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
                # logging.info(f"Order type Selected:{order_type}")

    
                # symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                # trading_bot.get_symbol_filters(symbol=symbol)
                # logging.info(f'Symbol Input {symbol}')


                # order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
                # logging.info(f"Order type Selected:{order_type}")

                # if order_type in ["MARKET", "LIMIT", "TWAP" , "EXIT"]:

                #     quantity = float(input("Quantity: ").strip())

                #     if quantity >= 0:
                #         logging.info(f"Quantity:{quantity}")
                # else:
                #     logging.info(f"Quantity:{quantity}")
                #     raise ValueError("Quantity can not be less than or equal to 0")
                

            # if order_type == "EXIT":
            #     print("Exiting bot.")
            #     logging.info(f'Bot Exit')
            #     break



        
        #     if order_type == "MARKET":
        #         response = trading_bot.place_fututres_order(symbol, side, quantity)
        #         logging.info(f"User Opted for Market. Response:{response}")

        #     elif order_type == "LIMIT":
        #         price = float(input("Limit Price: ").strip())
        #         logging.info(f"Price for LIMIT {price}")
        #         response = trading_bot.place_futures_limit_order(symbol, side, quantity, price)
        #         logging.info(f"User opted for LIMIT,Response: {response}")

        #     elif order_type == "TWAP":
        #         logging.info("User Opted TWAP")
        #         duration = int(input("Duration in seconds: ").strip())
        #         logging.info(f"TWAP Duration:{duration}")

        #         interval = int(input("Interval in seconds: ").strip())
        #         response = trading_bot.place_futures_twap_order(symbol, side, quantity, duration, interval)

        #     else:
        #         print("Invalid order type. Please try again.")
        #         continue

        #     print("Order Response:")
        #     print(response)
        #     logging.info(f"Order Response: {response}")

        # except Exception as e:
        #     print(f"Error: {e}")
        #     logging.error(f"Error Occured: {e}")
        #     raise

if __name__ == "__main__":
    main()



