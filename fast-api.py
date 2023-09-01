from fastapi import FastAPI, Query, Form
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import config
import certifi

app = FastAPI()

client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["sample_guides"]
col = db["planets"]

@app.get('/')
async def home():
    return JSONResponse(content={"message": "Welcome to the FastAPI Planets API!"})

@app.get('/planets_list')
async def get_planets():
    planets = [i['name'] for i in col.find({}, {'_id': 0})]
    return JSONResponse(content=planets, status_code=200)

@app.get('/planet_details')
async def get_planet_by_name(name: str = Query(..., description="The name of the planet to retrieve")):
    planet = col.find_one({"name": name}, {'_id': False})
    if not planet:
        return JSONResponse(content={"error": "Planet not found"}, status_code=404)
    return JSONResponse(content=planet, status_code=200)

@app.post('/create_planet')
async def create_planet(name: str = Form(..., description="The name of the planet to create")):
    if not name:
        return JSONResponse(content={"error": "Planet name is required"}, status_code=400)
    new_planet = {"name": name}
    col.insert_one(new_planet)
    return JSONResponse(content={"message": "Planet created successfully"}, status_code=201)

@app.put('/update_planet')
async def update_planet(name: str = Form(..., description="The name of the planet to update")):
    if not name:
        return JSONResponse(content={"error": "Planet name is required"}, status_code=400)

    # Replace the following placeholder with your actual update logic
    # Example:
    # col.update_one({"name": name}, {"$set": {"population": 1000000}})
    updated_planet = {"name": name, "message": "Planet updated successfully"}
    return JSONResponse(content=updated_planet, status_code=200)

@app.patch('/partially_update_planet')
async def partially_update_planet(name: str = Form(..., description="The name of the planet to partially update")):
    if not name:
        return JSONResponse(content={"error": "Planet name is required"}, status_code=400)

    # Replace the following placeholder with your actual partial update logic
    # Example:
    # col.update_one({"name": name}, {"$set": {"population": 1000000}})
    partially_updated_planet = {"name": name, "message": "Planet partially updated successfully"}
    return JSONResponse(content=partially_updated_planet, status_code=200)

@app.delete('/delete_planet')
async def delete_planet(name: str = Query(..., description="The name of the planet to delete")):
    if not name:
        return JSONResponse(content={"error": "Planet name is required"}, status_code=400)

    # Replace the following placeholder with your actual delete logic
    # Example:
    # col.delete_one({"name": name})
    return JSONResponse(content={"message": "Planet deleted successfully"}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
