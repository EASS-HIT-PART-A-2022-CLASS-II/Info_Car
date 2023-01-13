from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI, File
client=MongoClient("mongodb://localhost:27017")
db = client["car"]
async def upload_file(file: bytes = File(...)):
    # insert the file into the database
    result = db["files"].insert_one({"file": file})
    return {"file_id": str(result.inserted_id)}
