import os
import json
from tools.query import sql
from datetime import datetime
from dotenv import load_dotenv
from tools.prices import get_price_history
from tools.metadata import get_token_metadata
from tools.fetch_transactions import fetch_transactions_in_batches
from tools.database_operations import dump_to_cloudflare_r2, general_dump_to_cloudflare_r2

def main():
    load_dotenv()
    quicknode_client_url = os.getenv("QUICKNODE_CLIENT")
    access_key = os.getenv('CLOUDFLARE_ACCESS_KEY')
    secret_key = os.getenv('CLOUDFLARE_SECRET_KEY')
    bucket_name = "orca-sol-usdc"
    bucket_name_price = "token-price"
    bucket_name_metadata = "token-metadata"

    # Fetch transactions
    batched_transactions = fetch_transactions_in_batches(sql, quicknode_client_url)

    # Upload transactions to Cloudflare R2
    current_date = datetime.now().strftime("%Y-%m-%d")
    dump_to_cloudflare_r2(batched_transactions, access_key, secret_key, orca-sol-usdc, f"{current_date}2.json")
    print(f"Uploaded {len(batched_transactions)} records to Cloudflare R2")

    # Token Metadata
    metadata = get_token_metadata()
    metadata_data = json.dumps(metadata)
    general_dump_to_cloudflare_r2(metadata_data, access_key, secret_key, token-metadata, f"token_metadata.json")
    print(f"Uploaded {len(metadata)} record to Cloudflare R2")

    # Prices 
    sol_prices = get_price_history('solana', 1)
    sol_price_data = json.dumps(sol_prices)
    general_dump_to_cloudflare_r2(sol_price_data, access_key, secret_key, token-price, f"sol_price_{current_date}.json")
    usdc_prices = get_price_history('usd-coin', 1)
    usdc_price_data = json.dumps(usdc_prices)
    general_dump_to_cloudflare_r2(usdc_price_data, access_key, secret_key, token-price, f"usdc_price_{current_date}.json")

if __name__ == "__main__":
    main()
