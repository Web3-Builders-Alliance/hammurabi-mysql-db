import os
import json
import gzip
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.signature import Signature
from .query import get_transaction_hash
from .parse import response_to_dict
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_transaction(solana_client, tx_id):
    try:
        sig = Signature.from_string(tx_id)
        response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0).value
        return response_to_dict(response)
    except Exception as e:
        print(f"Error processing transaction ID: {tx_id}, {e}")
        return None

def fetch_transactions_in_batches(sql_query, quicknode_client_url):
    load_dotenv()

    tx_ids = get_transaction_hash(sql_query=sql_query)
    tx_df = pd.DataFrame(tx_ids.records)
    tx_id_list = tx_df['tx_id'].tolist()

    solana_client = Client(quicknode_client_url)

    total_transactions = len(tx_id_list)
    all_batch_results = []
    failed_tx_ids = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_tx_id = {executor.submit(fetch_transaction, solana_client, tx_id): tx_id for tx_id in tx_id_list}

        for future in as_completed(future_to_tx_id):
            tx_id = future_to_tx_id[future]
            try:
                response_dict = future.result()
                if response_dict:
                    all_batch_results.append(response_dict)
                else:
                    print(f"No valid response for transaction ID {tx_id}")
                    failed_tx_ids.append(tx_id)
            except Exception as e:
                print(f"Error processing transaction ID: {tx_id}, {e}")
                failed_tx_ids.append(tx_id)

    if failed_tx_ids:
        print("Retrying unsuccessful transaction calls")
        for tx_id in failed_tx_ids:
            response_dict = fetch_transaction(solana_client, tx_id)
            if response_dict:
                all_batch_results.append(response_dict)

    try:
        os.makedirs('data-seed', exist_ok=True)
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f'data-seed/all_batch_results_{current_date}.json.gz'
        with gzip.open(filename, 'wt', encoding='UTF-8') as f:
            json.dump(all_batch_results, f)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

    return all_batch_results

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
