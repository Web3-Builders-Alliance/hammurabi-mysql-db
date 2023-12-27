from pymongo import MongoClient
from datetime import datetime, timedelta

def delete_entries(mongo_uri, db_name, collection_name, date_field):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    ## Find date 30 days ago 
    past = datetime.now() - timedelta(days=30)
    past_timestamp = int(past.timestamp())

    ## Remove old documents
    query = {date_field: {"$lt": past_timestamp}}

    result = collection.delete_many(query)

    print(f"Deleted {result.deleted_count} records older than 30 days from the collection '{collection_name}' collection.")