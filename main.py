import os
import sys
import pymongo
from dotenv import load_dotenv
from tools.query import sql
from tools.database_operations import dump_to_mongodb
from tools.fetch_transactions import fetch_transactions_in_batches

def main():
    load_dotenv()
    quicknode_client_url = os.getenv("QUICKNODE_CLIENT")
    mongo_uri = os.getenv('MONGO_URI')
    db_name = 'Hammurabi'
    collection_name = 'orca'

    batched_transactions = fetch_transactions_in_batches(sql, quicknode_client_url)
    dump_to_mongodb(batched_transactions, mongo_uri, db_name, collection_name)
    print(f"Inserted {len(batched_transactions)} record into MongoDB")

if __name__ == "__main__":
    main()

## To Do
## 1. Write script that uploads spreadsheet to MongoDB. 
## 2. New batch for transactions that failed and try again - DONE
## 3. "Loading screen" for batch job - DONE 
## 4. Deduplication of Mongo DB on upload - DONE 
## 5. Instruction Decoding / Multi-Hop Counting 
## 6. Code linting - move parsing of RPC call to a new file - DONE
## 7. Database - delete all entries in Mongo that are older than 30 days old - DONE 
## 8. Backfill - grab all transactions to have 30 days worth of data
## 9. Quicknode API - get second key to try if first key hits a rate limit 
## 10. Set up second Mongo DB for data transformation