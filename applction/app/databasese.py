from pymongo import MongoClient
import pymongo
from gridfs import GridFS
from applction.app.databases1 import cars
# Create a client instance
#client = MongoClient("mongodb://localhost:27017/")
# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Get the database
db = client["mydatabase"]

# Get the collection
collection = db["mycollection"]
# cars = {
#     1: {
#         "make": "CarBrand",
#         "model": "Fast",
#         "year": 1998,
#         "price": 25000.0,
#         "engine": "V8",
#         "autonomous": False,
#         "sold": ["NA","EU"]
#     },

#     2: {
#         "make": "Speedy",
#         "model": "FourWheeler SUV",
#         "year": 2021,
#         "price": 55400.0,
#         "engine": "V4",
#         "autonomous": False,
#         "sold": ["AF","AN","AS","EU","NA","OC","SA"]
#     },

#     3: {
#         "make": "Elektrik",
#         "model": "AutoCar",
#         "year": 2019,
#         "price": 45000.0,
#         "engine": "V8",
#         "autonomous": True,
#         "sold": ["AS"]
#     },

#     4: {
#         "make": "CarBrand",
#         "model": "Beetle",
#         "year": 2004,
#         "price": 21299.99,
#         "engine": "V4",
#         "autonomous": False,
#         "sold": []
#     },

#     5: {
#         "make": "CarPro",
#         "model": "Supersonic",
#         "year": 2015,
#         "price": 215000.0,
#         "engine": "V12",
#         "autonomous": False,
#         "sold": ["NA","AF","OC","SA"]
#     }
# }
cars = {
    1: {
        "make": "CarBrand",
        "model": "Fast",
        "year": 1998,
        "price": 25000.0,
        "engine": "V8",
        "autonomous": False,
        "sold": ["NA","EU"]
    },

    2: {
        "make": "Speedy",
        "model": "FourWheeler SUV",
        "year": 2021,
        "price": 55400.0,
        "engine": "V4",
        "autonomous": False,
        "sold": ["AF","AN","AS","EU","NA","OC","SA"]
    },

    3: {
        "make": "Elektrik",
        "model": "AutoCar",
        "year": 2019,
        "price": 45000.0,
        "engine": "V8",
        "autonomous": True,
        "sold": ["AS"]
    },

    4: {
        "make": "CarBrand",
        "model": "Beetle",
        "year": 2004,
        "price": 21299.99,
        "engine": "V4",
        "autonomous": False,
        "sold": []
    },

    5: {
        "make": "CarPro",
        "model": "Supersonic",
        "year": 2015,
        "price": 215000.0,
        "engine": "V12",
        "autonomous": False,
        "sold": ["NA","AF","OC","SA"]
    }
}

collection.insert_one(cars);