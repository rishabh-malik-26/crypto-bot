# 💹 Binance Futures CLI Trading Bot (Testnet)

A simple, interactive command-line interface (CLI) trading bot for **Binance Futures Testnet**, written in Python.  
Supports **Market**, **Limit**, and **TWAP (Time-Weighted Average Price)** order types with validations like margin check, notional value, symbol existence, and more.

---

## 🚀 Features

- ✅ Connects to Binance USDT-M Futures Testnet
- ✅ Place **BUY** or **SELL** orders
- ✅ Supports:
  - Market Orders
  - Limit Orders
  - TWAP Orders (executed over time intervals)
- ✅ Checks:
  - Symbol availability
  - Min/Max quantity and price
  - Required vs. available margin
  - Notional value rules (e.g., `price × quantity ≥ 20 USDT`)
- ✅ Handles user input errors gracefully
- ✅ Exit anytime with `EXIT` or `QUIT`

---

## 🧑‍💻 Setup Instructions

### 1. Clone the Repo
# Clone the repo
git clone https://github.com/your-username/binance-futures-cli-bot.git
cd binance-futures-cli-bot

## pip install -r requirements.txt

# 🔑 Add your API keys in logic.py 
# Look for: API_KEY = "your_key" and API_SECRET = "your_secret"

# Run the bot
python bot.py
