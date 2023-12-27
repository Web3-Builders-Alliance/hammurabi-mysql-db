import requests
from datetime import datetime, timedelta

def get_price_history(coin_id, days=1, interval='hourly'): 
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': interval
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['price']

def print_price_history(coin_id, prices):
    print(f"Price history for {coin_id.upper()} in the last 24 hours (USD):")
    for price in prices:
        timestamp = datetime.fromtimestamp(price[0] / 1000)
        print(f"{timestamp}: ${price[1]:.4f}")

# Get historical prices
sol_prices = get_price_history('solana')
usdc_prices = get_price_history('usd-coin')

# Print the results
print_price_history('sol', sol_prices)
print_price_history('usdc', usdc_prices)