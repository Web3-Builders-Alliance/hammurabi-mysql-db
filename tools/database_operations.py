from pymongo import MongoClient

def dump_to_mongodb(all_batch_results, mongo_uri, db_name, collection_name): 
    client = MongoClient(mongo_uri)
    db = client.db_name
    collection = db["orca"]

    if all_batch_results: 
        collection.insert_many(all_batch_results)