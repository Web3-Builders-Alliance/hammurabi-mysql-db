import os
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.signature import Signature
from flipside_query import get_transaction_hash, sql

load_dotenv()

## Grab the Orca SOL <---> USDC transaction hashes from Flipside
tx_ids = get_transaction_hash(sql_query=sql)

quicknode_client = os.getenv(QUICKNODE_CLIENT)
solana_client = Client(quicknode_client)

## Process in batches of 1000
for chunk in chunk_list(tx_ids, 1000): 
    batch_results = []
    for tx_id in chunk: 
        try: 
            sig = Signature.from_string(tx_id)
            response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0)
            batch_results.append(response)
        except Exception as e: 
            print(f"Error processing transaction ID {tx_id}: {e}")
    print(batch_results)

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]