import os
import requests
import csv
from dotenv import load_dotenv
from datetime import datetime

def get_price_history(coin_id, days=30):
    load_dotenv()
    api_key = os.getenv('COINGECKO_API_KEY')

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data['prices']

def save_price_history_to_csv(coin_id, prices):
    with open(f'{coin_id}_price_history.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Token', 'Price', 'Timestamp'])

        for price_data in prices:
            timestamp = datetime.utcfromtimestamp(price_data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            price = price_data[1]
            writer.writerow([coin_id.upper(), price, timestamp])
