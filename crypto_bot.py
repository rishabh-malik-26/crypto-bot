from scalable import bot
import logging
logging.basicConfig(
    level=logging.INFO,   
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_bot.log',
    filemode="a")


def main():
    print("=== Welcome to Binance Futures CLI Bot ===")

    while True:
        try:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            bot.validate_symbol(symbol=symbol)
            logging.info(f'Symbol Added {symbol}')

            side = input("Side (BUY or SELL): ").strip().upper()
            logging.info(f'Side Added {symbol}')

            order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
            logging.info(f"Order type Selected:{order_type}")

            if order_type == "EXIT":
                print("Exiting bot.")
                logging.info(f'Bot Exit')
                break

            quantity = float(input("Quantity: ").strip())
            logging.info(f"Quantity:{quantity}")

            if order_type == "MARKET":
                response = bot.place_spot_market_order(symbol, side, quantity)
                logging.info(f"User Opted for Market. Response:{response}")

            elif order_type == "LIMIT":
                price = float(input("Limit Price: ").strip())
                logging.info(f"Price for LIMIT {price}")
                response = bot.place_futures_limit_order(symbol, side, quantity, price)
                logging.info(f"User opted for LIMIT,Response: {response}")

            elif order_type == "TWAP":
                logging.info("User Opted TWAP")
                duration = int(input("Duration in seconds: ").strip())
                logging.info(f"TWAP Duration:{duration}")

                interval = int(input("Interval in seconds: ").strip())
                response = bot.place_futures_twap_order(symbol, side, quantity, duration, interval)

            else:
                print("Invalid order type. Please try again.")
                continue

            print("Order Response:")
            print(response)
            logging.info(f"Order Response: {response}")

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error Occured: {e}")
            raise

if __name__ == "__main__":
    main()











# def main():
#     print("=== Welcome to Binance Futures CLI Bot ===")
#     while True:
#         try:
#             symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
#             logging.info(f'Symbol Added: {symbol}')
            
#             side = input("Side (BUY or SELL): ").strip().upper()
#             logging.info(f'Side Added: {side}')  # Fixed: was logging {symbol} instead of {side}
            
#             order_type = input("Order Type (MARKET / LIMIT / TWAP / EXIT): ").strip().upper()
#             logging.info(f"Order type Selected: {order_type}")
            
#             if order_type == "EXIT":
#                 print("Exiting bot.")
#                 logging.info('Bot Exit')
#                 break
            
#             quantity = float(input("Quantity: ").strip())
#             logging.info(f"Quantity: {quantity}")
            
#             if order_type == "MARKET":
#                 response = bot.place_spot_market_order(symbol, side, quantity)
#                 logging.info(f"User Opted for Market. Response: {response}")
                
#             elif order_type == "LIMIT":
#                 price = float(input("Limit Price: ").strip())
#                 logging.info(f"Price for LIMIT: {price}")
#                 response = bot.place_futures_limit_order(symbol, side, quantity, price)
#                 logging.info(f"User opted for LIMIT, Response: {response}")
                
#             elif order_type == "TWAP":
#                 logging.info("User Opted TWAP")
#                 duration = int(input("Duration in seconds: ").strip())
#                 logging.info(f"TWAP Duration: {duration}")
#                 interval = int(input("Interval in seconds: ").strip())
#                 logging.info(f"TWAP Interval: {interval}")  # Added missing logging
#                 response = bot.place_futures_twap_order(symbol, side, quantity, duration, interval)
#                 logging.info(f"User opted for TWAP, Response: {response}")  # Added missing logging
                

#             else:
#                 print("Invalid order type. Please try again.")
#                 logging.warning("Invalid order type entered")  
#                 continue
                
#             print("Order Response:")
#             print(response)
#             logging.info(f"Order Response: {response}")
            
#         except Exception as e:
#             print(f"Error: {e}")
#             logging.error(f"Error Occurred: {e}")
#             raise

# if __name__ == "__main__": 
#     main()

# import logging
# import json 
# logging.basicConfig(
#     level=logging.INFO,   
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filename='crypto_bot.log',
#     filemode="a")
# from binance import Client
# from datetime import datetime
# from binance.exceptions import BinanceAPIException, BinanceOrderException
# from scalable import BasicBot
# import time
# import math

# def validate_input(prompt, input_type=str, valid_options=None):
#     """Validate user input with type checking and options"""
#     while True:
#         try:
#             user_input = input(prompt).strip()
            
#             if input_type == float:
#                 value = float(user_input)
#                 if value <= 0:
#                     print("Please enter a positive number.")
#                     continue
#                 return value
#             elif input_type == int:
#                 value = int(user_input)
#                 if value <= 0:
#                     print("Please enter a positive integer.")
#                     continue
#                 return value
#             else:
#                 value = user_input.upper()
#                 if valid_options and value not in valid_options:
#                     print(f"Please enter one of: {', '.join(valid_options)}")
#                     continue
#                 return value
                
#         except ValueError:
#             print(f"Please enter a valid {input_type.__name__}.")
#         except KeyboardInterrupt:
#             print("\nExiting...")
#             exit()

# def main():
#     print("=" * 50)
#     print("    BINANCE FUTURES TRADING BOT (TESTNET)")
#     print("=" * 50)
    
#     # Initialize bot with your API credentials
#     # Replace with your actual testnet API credentials

#     try:
#         bot = BasicBot(API_KEY, API_SECRET, testnet=True)
#         logging.info("Bot initialized successfully")
        
#         # Show account balance
#         balance = bot.get_account_balance()
#         if balance:
#             print(f"\nAccount Balance: {balance['total_balance']} USDT")
        
#     except Exception as e:
#         logging.error(f"Failed to initialize bot: {e}")
#         print("Error: Could not connect to Binance API. Please check your credentials.")
#         return
    
#     while True:
#         try:
#             print("\n" + "=" * 50)
#             print("TRADING OPTIONS:")
#             print("1. MARKET - Market Order")
#             print("2. LIMIT - Limit Order") 
#             print("3. TWAP - Time-Weighted Average Price")
#             print("4. STOP_LIMIT - Stop-Limit Order (Advanced)")
#             print("5. BALANCE - Check Account Balance")
#             print("6. ORDERS - View Open Orders")
#             print("7. EXIT - Exit Bot")
#             print("=" * 50)
            
#             choice = validate_input("Select option (1-7): ", str, ['1', '2', '3', '4', '5', '6', '7'])
            
#             if choice == '7':
#                 print("Exiting bot. Goodbye!")
#                 logging.info("Bot exit requested by user")
#                 break
#             elif choice == '5':
#                 balance = bot.get_account_balance()
#                 if balance:
#                     print(f"\nTotal Balance: {balance['total_balance']} USDT")
#                     print(f"Available Balance: {balance['available_balance']} USDT")
#                 continue
#             elif choice == '6':
#                 orders = bot.get_open_orders()
#                 if orders:
#                     print(f"\nOpen Orders ({len(orders)}):")
#                     for order in orders:
#                         print(f"  {order['symbol']} {order['side']} {order['type']} - {order['origQty']} @ {order.get('price', 'MARKET')}")
#                 else:
#                     print("No open orders.")
#                 continue
            
#             # Get trading parameters
#             symbol = validate_input("Enter symbol (e.g., BTCUSDT): ")
            
#             # Validate symbol
#             if not bot.validate_symbol(symbol):
#                 print("Invalid symbol. Please try again.")
#                 continue
            
#             side = validate_input("Side (BUY/SELL): ", str, ['BUY', 'SELL'])
#             quantity = validate_input("Quantity: ", float)
            
#             # Execute based on choice
#             if choice == '1':  # MARKET
#                 response = bot.place_futures_market_order(symbol, side, quantity)
                
#             elif choice == '2':  # LIMIT
#                 price = validate_input("Limit Price: ", float)
#                 response = bot.place_futures_limit_order(symbol, side, quantity, price)
                
#             elif choice == '3':  # TWAP
#                 duration = validate_input("Duration in seconds: ", int)
#                 interval = validate_input("Interval in seconds: ", int)
#                 if interval > duration:
#                     print("Interval cannot be greater than duration.")
#                     continue
#                 response = bot.place_futures_twap_order(symbol, side, quantity, duration, interval)
                
#             elif choice == '4':  # STOP_LIMIT
#                 stop_price = validate_input("Stop Price: ", float)
#                 limit_price = validate_input("Limit Price: ", float)
#                 response = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
            
#             # Display results
#             print("\n" + "=" * 30)
#             print("ORDER EXECUTION RESULT:")
#             print("=" * 30)
#             print(json.dumps(response, indent=2))
            
#             if response['status'] == 'SUCCESS':
#                 print("✅ Order executed successfully!")
#             else:
#                 print("❌ Order failed!")
                
#         except KeyboardInterrupt:
#             print("\nExiting...")
#             break
#         except Exception as e:
#             logging.error(f"Error in main loop: {e}")
#             print(f"Error: {e}")

# if __name__ == "__main__":
#     main()