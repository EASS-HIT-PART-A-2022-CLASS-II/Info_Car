from fastapi import FastAPI, Query, Path, HTTPException, status, Body, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from starlette.responses import HTMLResponse
from starlette.status import HTTP_400_BAD_REQUEST
from db import cars
from pymongo import MongoClient
import json
import pymongo
#from applction.app.db import conn
#from routes.user import user
#import pymongo
templates = Jinja2Templates(directory="templates")
 # Connect to the MongoDB instance
client = pymongo.MongoClient("mongodb+srv://oritskovich:S8QlGyGKXRe72I8x@oritskovich.iewit1v.mongodb.net/?retryWrites=true&w=majority")
   # Select the database and collection
db = client["cars"]
cars_collection = db["car"]
 
class Car(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int] = Field(...,ge=1970,lt=2022)
    price: Optional[float]
    engine: Optional[str] = "V4"
    autonomous: Optional[bool]
    sold: Optional[List[str]]

app = FastAPI()
#app.include_router(user)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=RedirectResponse)
def root(request: Request):
    return RedirectResponse(url="/cars")

@app.get("/cars", response_class=HTMLResponse)
def get_cars(request: Request, number: Optional[str] = Query("10",max_length=3)):
    response = []
    for id, car in list(cars.items())[:int(number)]:
        response.append((id,car))
    return templates.TemplateResponse("index.html", {"request": request, "cars": response, "title": "Home"})

@app.post("/search", response_class=RedirectResponse)
def search_cars(id: str = Form(...)):
    car = cars_collection.find_one({"id": id})
    if car:
        return RedirectResponse("/cars/" + id, status_code=302)
    else:
        return {"error": "Car not found"}

@app.get("/cars/{id}", response_class=HTMLResponse)
def get_car_by_id(request: Request, id: int = Path(...,ge=0,lt=1000)):
    car = cars.get(id)
    response = templates.TemplateResponse("search.html", {"request": request, "car": car, "id": id, "title": "Search Car"})
    if not car:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

@app.get("/create", response_class=HTMLResponse)
def create_car(request: Request):
    return templates.TemplateResponse("create.html", {"request": request, "title": "Create Car"})

@app.get("/edit", response_class=HTMLResponse)
def edit_car(request: Request, id: int = Query(...)):
    # Find the car document by ID
    car = cars_collection.find_one({"id": id})
    if not car:
     return templates.TemplateResponse("search.html", {"request": request, "id": id, "car": car, "title": "Edit Car"}, status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("edit.html", {"request": request, "id": id, "car": car, "title": "Edit Car"})

@app.post("/cars/{id}")
def update_car(request: Request, id: int,
    make: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    year: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    engine: Optional[str] = Form(None),
    autonomous: Optional[bool] = Form(None),
    sold: Optional[List[str]] = Form(None),):
    stored = cars.get(id)
    if not stored:
        return templates.TemplateResponse("search.html", {"request": request, "id": id, "car": stored, "title": "Edit Car"}, status_code=status.HTTP_404_NOT_FOUND)
    stored = Car(**dict(stored))
    car = Car(make=make,model=model,year=year,price=price,engine=engine,autonomous=autonomous,sold=sold)
    new = car.dict(exclude_unset=True)
    new = stored.copy(update=new)
    cars[id] = jsonable_encoder(new)
    response = {}
    response[id] = cars[id]
    return RedirectResponse(url="/cars", status_code=302)


@app.get("/delete/{id}", response_class=RedirectResponse)
def delete_car(request: Request, id: int = Path(...)):
    # Delete the car
    result = cars_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        return templates.TemplateResponse("search.html", {"request": request, "id": id, "title": "Edit Car"}, status_code=status.HTTP_404_NOT_FOUND)
        del cars[id]
    return RedirectResponse(url="/cars")
