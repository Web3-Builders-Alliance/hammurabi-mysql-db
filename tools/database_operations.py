from pymongo import MongoClient

def dump_to_mongodb(all_batch_results, mongo_uri, db_name, collection_name): 
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for result in all_batch_results:
        signature = result['transaction']['signatures'][0] if result['transaction']['signatures'] else None
        if signature:
            existing_entry = collection.find_one({"transaction.signatures": signature})
            if existing_entry:
                print(f"Duplicate entry found, did not add entry with signature: {signature}")
            else:
                collection.insert_one(result)
                print(f"Inserted new entry with signature: {signature}")
