import pymongo
from dotenv import load_dotenv
import sys
import os

load_dotenv()
uri = os.getenv('MONGO_URI')

# Create new client and connect to the server
try:
    client = pymongo.MongoClient(uri)

except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Check if Atlas host name / password is correct in the connection string")
    sys.exit(1)

# Use the Hammurabi Database
db = client.Hammurabi

# Use the Orca Collection
orca_collection = db["orca"]