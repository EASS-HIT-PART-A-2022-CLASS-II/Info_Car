import pymongo
try:
    # Connect to the MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print("Connection to MongoDB successful!")

except pymongo.errors.ConnectionFailure as e:
    print("Connection to MongoDB failed:", e)