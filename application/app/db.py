import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")
db = client["cars"]
collection = db["car"]
my_dict_list = [ {
        "make": "CarBrand",
        "model": "Fast",
        "year": 1998,
        "price": 25000.0,
        "engine": "V8",
        "autonomous": False,
        "sold": ["NA","EU"]
    },
    {
      
        "make": "Speedy",
        "model": "FourWheeler SUV",
        "year": 2021,
        "price": 55400.0,
        "engine": "V4",
        "autonomous": False,
        "sold": ["AF","AN","AS","EU","NA","OC","SA"]
    },

    {
        
        "make": "Elektrik",
        "model": "AutoCar",
        "year": 2019,
        "price": 45000.0,
        "engine": "V8",
        "autonomous": True,
        "sold": ["AS"]
    },

     {
        
        "make": "CarBrand",
        "model": "Beetle",
        "year": 2004,
        "price": 21299.99,
        "engine": "V4",
        "autonomous": False,
        "sold": []
    },

     {
        "make": "CarPro",
        "model": "Supersonic",
        "year": 2015,
        "price": 215000.0,
        "engine": "V12",
        "autonomous": False,
        "sold": ["NA","AF","OC","SA"]
    }
]
# Create a variable to store the current index
counter = 1
for item in my_dict_list:
    item["_id"] = counter
    counter += 1
collection.insert_many(my_dict_list)




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
