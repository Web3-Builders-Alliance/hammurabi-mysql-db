from pymongo import MongoClient

def delete_all_records(mongo_uri, db_name, collection_name): 
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    result = collection.delete_many({})

    print(f"Deleted {result.deleted_count} records from {collection}")