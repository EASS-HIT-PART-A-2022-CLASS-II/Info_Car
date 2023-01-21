import pymongo
from pymongo import MongoClient
import json
from databases import cars

client = pymongo.MongoClient("mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")
#db = client.test
db = client["cars"]
collection = db["car"]

# Create a variable to store the current index
index = 0

# Use the update_many() method to update the documents in the collection
collection.update_many({}, {"$set": {"id": index}})

# Iterate through the documents in the collection
for doc in collection.find():
    # Increment the index variable
    index += 1
    # Update the document with the new index
    collection.update_one({"_id": doc["_id"]}, {"$set": {"id": index}})
with open('cars.json') as f:
    data = json.loads(f.read())

data_list = list(data.values())
collection.insert_many(data_list)
