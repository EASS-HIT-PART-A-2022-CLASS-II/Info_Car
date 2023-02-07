from fastapi import FastAPI, Query, Path, HTTPException, status, Body, Request, Form, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from starlette.responses import HTMLResponse
from starlette.status import HTTP_400_BAD_REQUEST
from databases import cars
from pymongo import MongoClient
import json
import pymongo
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader


# from applction.app.db import conn
# from routes.user import user
# import pymongo
templates = Jinja2Templates(directory="templates")
# Connect to the MongoDB instance
client = pymongo.MongoClient(
    "mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")
# Select the database and collection
db = client["cars"]
cars_collection = db["car"]


class Car(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int] = Field(..., ge=1970, lt=2022)
    price: Optional[float]
    engine: Optional[str] = "V4"
    autonomous: Optional[bool]
    sold: Optional[List[str]]


app = FastAPI()
# app.include_router(user)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=RedirectResponse)
def root(request: Request):
    return RedirectResponse(url="/cars")


@app.get("/cars", response_class=HTMLResponse)
def get_cars(request: Request, number: Optional[str] = Query("10", max_length=3)):
    response = []
    for id, car in list(cars.items())[:int(number)]:
        response.append((id, car))
    return templates.TemplateResponse("index.html", {"request": request, "cars": response, "title": "Home"})


@app.post("/search",response_class=RedirectResponse)
def search_cars(id: str = Form(...)):
    return RedirectResponse("/cars/"+id,status_code=302)


@app.get("/cars/{id}", response_class=HTMLResponse)
def get_car_by_id(request: Request, id: int = Path(..., ge=0, lt=1000)):
    car = cars.get(id)
    response = templates.TemplateResponse(
        "search.html", {"request": request, "car": car, "id": id, "title": "Search Car"})
    if not car:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.post("/cars", status_code=status.HTTP_201_CREATED)
def add_cars(
    make: Optional[str] = Form(...),
    model: Optional[str] = Form(...),
    year: Optional[str] = Form(...),
    price: Optional[float] = Form(...),
    engine: Optional[str] = Form(...),
    autonomous: Optional[bool] = Form(...),
    sold: Optional[List[str]] = Form(None),
    min_id: Optional[int] = Body(0)):
    body_cars = [Car(make=make,model=model,year=year,price=price,engine=engine,autonomous=autonomous,sold=sold)]
    if len(body_cars) < 1:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,detail="No cars to add.")
    min_id = len(cars.values()) + min_id
    for car in body_cars:
         while cars.get(min_id):
          min_id += 1
          cars[min_id] = car
          min_id += 1
          cars_collection.insert_one(car.dict())
    return RedirectResponse(url="/cars", status_code=302)


# @app.post("/cars", status_code=status.HTTP_201_CREATED)
# def add_cars(
#     make: Optional[str] = Form(...),
#     model: Optional[str] = Form(...),
#     year: Optional[str] = Form(...),
#     price: Optional[float] = Form(...),
#     engine: Optional[str] = Form(...),
#     autonomous: Optional[bool] = Form(...),
#     sold: Optional[List[str]] = Form(None),
#     min_id: Optional[int] = Body(0)):
#     body_cars = [Car(make=make,model=model,year=year,price=price,engine=engine,autonomous=autonomous,sold=sold)]
#     if len(body_cars) < 1:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST,detail="No cars to add.")
#     min_id = len(cars.values()) + min_id
#     for car in body_cars:
#         while cars.get(min_id):
#             min_id += 1
#         cars[min_id] = car
#         min_id += 1
#     return RedirectResponse(url="/cars", status_code=302)




@app.get("/create", response_class=HTMLResponse)
def create_car(request: Request):
    return templates.TemplateResponse("create.html", {"request": request, "title": "Create Car"})

@app.post("/cars")
async def create_car(request: Request):
    
    form_data = await request.form()
    make = form_data.get("make")
    model = form_data["model"]
    year = int(form_data["year"])
    price = float(form_data["price"])
    engine =form_data["engine"]
    autonomous = form_data["autonomous"] == "true"
    sold = form_data.getlist("sold")

    car = {
        "make": make,
        "model": model,
        "year": year,
        "price": price,
        "engine": engine,
        "autonomous": autonomous,
        "sold": sold,
    }
    cars_collection.insert_one(car)

    return {"message": "Car created"}
@app.get("/edit",response_class=HTMLResponse)
def edit_car(request: Request, id: int = Query(...)):
    car = cars.get(id)
    if not car:
        return templates.TemplateResponse("search.html",{"request": request,"car":car,"id":id,"title": "Edit Car"},status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("edit.html",{"request": request,"id":id,"car":car,"title":"Edit car"})

@app.post("/cars/{id}")
def update_car(request: Request, id: int, make: Optional[str] = Form(None),
               model: Optional[str] = Form(None),
               year: Optional[str] = Form(None),
               price: Optional[float] = Form(None),
               engine: Optional[str] = Form(None),
               autonomous: Optional[bool] = Form(None),
               sold: Optional[List[str]] = Form(None),
               min_id: Optional[int] = Body(0)):
             
    client = pymongo.MongoClient( "mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")                                
# Select the database and collection
    db = client["cars"]
    cars_collection = db["car"]
    car = cars_collection.find_one({"_id": id})
    if not car:
        return templates.TemplateResponse("search.html",{"request": request,"car":car,"id":id,"title": "Edit Car"},status_code=status.HTTP_404_NOT_FOUND)
    if make:
        car["make"] = make
    if model:
        car["model"] = model
    if year:
        car["year"] = year
    if price:
        car["price"] = price
    if engine:
        car["engine"] = engine
    if autonomous:
        car["autonomous"] = autonomous
    if sold:
        car["sold"] = sold
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"make": make}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"model": model}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"year": year}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"price": price}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"engine": engine}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"autonomous": autonomous}})
    cars_collection.update_one({"_id": car["_id"]}, {"$set": {"sold": sold}})
    return car


@app.get("/delete/{id}", response_class=RedirectResponse)
def delete_car(request: Request, id: int = Path(...)):
    # Delete the car
    result = cars_collection.delete_one({"_id": id})
    if result.deleted_count == 0:
        return templates.TemplateResponse("search.html", {"request": request, "_id": id, "title": "Edit Car"}, status_code=status.HTTP_404_NOT_FOUND)
        del cars[_id]
    return RedirectResponse(url="/cars")
