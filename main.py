import os
import json
from dotenv import load_dotenv
from tools.query import sql
from tools.database_operations import dump_to_cloudflare_r2
from tools.fetch_transactions import fetch_transactions_in_batches

def main():
    load_dotenv()
    quicknode_client_url = os.getenv("QUICKNODE_CLIENT")
    access_key = os.getenv('CLOUDFLARE_ACCESS_KEY')
    secret_key = os.getenv('CLOUDFLARE_SECRET_KEY')
    bucket_name = os.getenv('CLOUDFLARE_BUCKET_NAME')

    db_name = 'Hammurabi'
    collection_name = 'orca'
    signature_record_file = "signature_record.json"

    # Read existing signatures
    if os.path.exists(signature_record_file):
        with open(signature_record_file, 'r') as file:
            existing_signatures = json.load(file)
    else:
        existing_signatures = []

    # Fetch transactions
    batched_transactions = fetch_transactions_in_batches(sql, quicknode_client_url)

    # Extract new signatures and update the list
    new_signatures = [trans['transaction']['signatures'][0] for trans in batched_transactions if trans['transaction']['signatures']]
    updated_signatures = list(set(existing_signatures + new_signatures))

    # Save updated signatures
    with open(signature_record_file, 'w') as file:
        json.dump(updated_signatures, file)

    # Upload to Cloudflare R2
    dump_to_cloudflare_r2(batched_transactions, access_key, secret_key, bucket_name, f"{collection_name}.json", signature_record_file)
    print(f"Uploaded {len(batched_transactions)} records to Cloudflare R2")

if __name__ == "__main__":
    main()
