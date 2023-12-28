import os
import json
from dotenv import load_dotenv
from tools.query import sql
from tools.database_operations import dump_to_cloudflare_r2, general_dump_to_cloudflare_r2
from tools.fetch_transactions import fetch_transactions_in_batches
from tools.metadata import get_token_metadata
from datetime import datetime

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

    # Token Metadata
    metadata = get_token_metadata()
    metadata_data = json.dumps(metadata)
    general_dump_to_cloudflare_r2(metadata_data, access_key, secret_key, bucket_name_metadata, f"token_metadata.json")
    print(f"Uploaded {len(metadata)} record to Cloudflare R2")

    # Upload to Cloudflare R2
    current_date = datetime.now().strftime("%Y-%m-%d")
    dump_to_cloudflare_r2(batched_transactions, access_key, secret_key, bucket_name, f"{current_date}.json")
    print(f"Uploaded {len(batched_transactions)} records to Cloudflare R2")

if __name__ == "__main__":
    main()
