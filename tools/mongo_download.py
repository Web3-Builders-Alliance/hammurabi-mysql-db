import os
import csv
from dotenv import load_dotenv
from pymongo import MongoClient

def fetch_data_from_mongo(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Fetch all documents from the collection
    return list(collection.find())

def convert_to_csv(data, csv_file_path):
    # Assuming data is a list of dictionaries
    keys = data[0].keys()  # Extracting the field names

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    db_name = 'Hammurabi'
    collection_name = 'orca'
    csv_file_path = 'data-seed/mongo_results.csv'

    data = fetch_data_from_mongo(mongo_uri, db_name, collection_name)
    convert_to_csv(data, csv_file_path)

    print(f"Data exported to {csv_file_path}")

if __name__ == "__main__":
    main()
