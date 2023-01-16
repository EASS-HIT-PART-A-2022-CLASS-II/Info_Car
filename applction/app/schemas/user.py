def carEntity(item)-> dict:
    return{
    "make": str(item["_make"]),
    "model":  str(item["model"]),
    "year": int(item[ "year"]),
    "price": float(item[ "price"]),
    "engine":  str(item[ "engine"]),
    "autonomous": bool(item["autonomous"]),
    "sold": str(item[ "sold"]),
    }

def carsEntity(entity)->list:
    return [carEntity(item) for item in entity]