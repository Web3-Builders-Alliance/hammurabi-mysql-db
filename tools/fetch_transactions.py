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

    # Console status counters
    total_transactions = len(tx_id_list)
    processed_transactions = 0

    # Process transactions in batches
    all_batch_results = []
    failed_tx_ids = []
    for chunk in chunk_list(tx_id_list, 5): 
        batch_results = []
        for tx_id in chunk: 
            try: 
                sig = Signature.from_string(tx_id)
                response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0).value
                
                # Convert response to dict
                response_dict = response_to_dict(response)
                if response_dict:
                    batch_results.append(response_dict)
                else:
                    print(f"No valid response for transaction ID {tx_id}")
            except Exception as e: 
                print(f"Error processing transaction ID: {tx_id}")
                failed_tx_ids.append(tx_id)
            finally: 
                processed_transactions += 1
                remaining = total_transactions - processed_transactions
                print(f"Processed: {processed_transactions}/{total_transactions}, Remaining: {remaining}")
        all_batch_results.extend(batch_results)

    ## Retry failed transaction IDs 
    if failed_tx_ids: 
        print("Retrying unsuccessful transaction calls")
        for tx_id in failed_tx_ids: 
            try: 
                sig = Signature.from_string(tx_id)
                response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0).value
                response_dict = response_to_dict(response)
                if response_dict:
                    batch_results.append(response_dict)
                else: 
                    print(f"No valid response for transactions ID: {tx_id}")
            except Exception as e: 
                print(f"Failed again to process transaction ID: {tx_id}")

    ## Save to data-seed folder in case database upload fails 
    try: 
        os.makedirs('data-seed', exist_ok=True)
        with open('data-seed/all_batch_results.json', 'w') as f:
            json.dump(all_batch_results, f)
    except Exception as e: 
        print(f"Error saving data to file: {e}")
    print(type(all_batch_results))
    return all_batch_results

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def response_to_dict(response): 
    if isinstance(response, str): 
        try:
            return json.loads(response)
        except json.JSONDecodeError: 
            print("Error decoding JSON response")
            return None
    elif hasattr(response, '__dict__'): 
        return response.__dict__
    else: 
        return response
