# while True:
#     try:
#         quantity = float(input("Enter quantity: "))
#         if quantity <= 0:
#             raise ValueError("Quantity must be greater than 0.")
#         break
#     except ValueError as e:
#         print(f"Invalid input: {e}")


def get_valid_input(prompt, expected_type=float, condition=lambda x: True, error_msg="Invalid input."):
    while True:
        try:
            value = expected_type(input(prompt).strip())
            if condition(value):
                return value
            else:
                print(error_msg)
        except ValueError:
            print("Please enter a valid", expected_type.__name__)

def show_help():
    """Display help information for the bot"""
    print("\n=== HELP ===")
    print("Main Menu Commands:")
    print("  BUY    - Place a buy order")
    print("  SELL   - Place a sell order")
    print("  HELP   - Show this help menu")
    print("  QUIT   - Exit the bot")
    print("  EXIT   - Exit the bot")
    print("\nOrder Type Commands (in BUY menu):")
    print("  MARKET - Place a market order")
    print("  LIMIT  - Place a limit order")
    print("  TWAP   - Place a TWAP order")
    print("  BACK   - Return to main menu")
    print("  QUIT   - Exit the bot")
    print("  EXIT   - Exit the bot")
    print("=============\n")

def confirm_action(action):
    """Get user confirmation for destructive actions"""
    while True:
        confirm = input(f"Are you sure you want to {action}? (YES/NO): ").strip().upper()
        if confirm in ["YES", "Y"]:
            return True
        elif confirm in ["NO", "N"]:
            return False
        else:
            print("Please enter YES or NO")

