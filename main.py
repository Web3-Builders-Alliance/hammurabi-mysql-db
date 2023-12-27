import os
import json
from dotenv import load_dotenv
from tools.query import sql
from tools.database_operations import dump_to_cloudflare_r2
from tools.fetch_transactions import fetch_transactions_in_batches
from datetime import datetime

def main():
    load_dotenv()
    quicknode_client_url = os.getenv("QUICKNODE_CLIENT")
    access_key = os.getenv('CLOUDFLARE_ACCESS_KEY')
    secret_key = os.getenv('CLOUDFLARE_SECRET_KEY')
    bucket_name = "orca-sol-usdc"

    # Fetch transactions
    batched_transactions = fetch_transactions_in_batches(sql, quicknode_client_url)

    # Upload to Cloudflare R2
    current_date = datetime.now().strftime("%Y-%m-%d")
    dump_to_cloudflare_r2(batched_transactions, access_key, secret_key, bucket_name, f"{current_date}2.json")
    print(f"Uploaded {len(batched_transactions)} records to Cloudflare R2")

if __name__ == "__main__":
    main()
