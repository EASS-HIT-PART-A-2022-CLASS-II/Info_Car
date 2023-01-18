from pymongo import MongoClient
import json
import pymongo
from databases import cars

client = pymongo.MongoClient("mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")
#db = client.test
db = client["cars"]
collection = db["car"]
with open('cars.json') as f:
    data = json.loads(f.read())

data_list = list(data.values())
collection.insert_many(data_list)
