import os
import json
import pandas as pd
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.signature import Signature
from .query import get_transaction_hash

def fetch_transactions_in_batches(sql_query, quicknode_client_url):
    # Load environment variables
    load_dotenv()

    # Get transaction IDs
    tx_ids = get_transaction_hash(sql_query=sql_query)
    tx_df = pd.DataFrame(tx_ids.records)
    tx_id_list = tx_df['tx_id'].tolist()

    # Initialize Solana client
    solana_client = Client(quicknode_client_url)

    # Process transactions in batches
    all_batch_results = []
    for chunk in chunk_list(tx_id_list, 1000): 
        batch_results = []
        for tx_id in chunk: 
            try: 
                sig = Signature.from_string(tx_id)
                response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0)
                batch_results.append(response)
            except Exception as e: 
                print(f"Error processing transaction ID {tx_id}: {e}")
        all_batch_results.extend(batch_results)

    ## Save to data-seed folder incase database upload fails 
    try: 
        os.makedirs('data-seed', exist_ok=True)
        with open('data-seed/all_batch_results.json', 'w') as f:
            json.dump(all_batch_results, f)
    except Exception as e: 
        print(f"Error saving data to file: {e}")
    
    return all_batch_results

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## Need to save the transaction IDs that fail and then try them again at the end in a new batch 