from fastapi import APIRouter
from models.user import Car
from applction.app.db import conn
from schemas.user import carEntity,carsEntity
user =APIRouter()
@user.get('/')
def find_all_car():
 print(conn.local.user.find())
 print(carsEntity(conn.local.car.find())) 
 return carsEntity(conn.local.car.find()) 