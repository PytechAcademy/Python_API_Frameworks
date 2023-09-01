from flask import Flask, jsonify, redirect, request
from pymongo import MongoClient
import config
import certifi
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

client = MongoClient(config.MONGO_URI,tlsCAFile=certifi.where())
db = client["sample_guides"]
col = db["planets"]

@app.route('/')
def home():
    return redirect("/apidocs")

@app.route('/planets_list',methods=['GET'])
def get_planets():
    """
        Get a list of all planets.
        ---
        responses:
          200:
            description: A list of planet names.
        """
    planets = [i['name'] for i in col.find({},{'_id':0})]
    return jsonify(planets)

@app.route('/planet_details', methods=['GET'])
def get_planet_by_name():
    """
    Get a planet based on its name.
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the planet to retrieve.
    responses:
      200:
        description: Planet retrieved successfully.
      400:
        description: Planet name is required.
      404:
        description: Planet not found.
    """
    planet_name = request.args.get('name')
    if not planet_name:
        return jsonify({"error": "Planet name is required"}), 400
    planet = col.find_one({"name": planet_name}, {'_id': False})
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet), 200


@app.route('/create_planet', methods=['POST'])
def create_planet():
    """
    Create a new planet.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the planet to create.
    responses:
      201:
        description: Planet created successfully.
      400:
        description: Bad request. Planet name is required.
    """
    planet_name = request.form.get('name')
    if not planet_name:
        return jsonify({"error": "Planet name is required"}), 400
    new_planet = {"name": planet_name}
    col.insert_one(new_planet)
    return jsonify({"message": "Planet created successfully"}), 201


@app.route('/update_planet', methods=['PUT'])
def update_planet():
    """
    Update a planet.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the planet to update.
    responses:
      200:
        description: Planet updated successfully.
      400:
        description: Bad request. Planet name is required.
      404:
        description: Planet not found.
    """
    planet_name = request.form.get('name')
    if not planet_name:
        return jsonify({"error": "Planet name is required"}), 400

    # Replace the following placeholder with your actual update logic
    # Example:
    # col.update_one({"name": planet_name}, {"$set": {"population": 1000000}})

    # Check if the planet was updated successfully and return the appropriate response


@app.route('/partially_update_planet', methods=['PATCH'])
def partially_update_planet():
    """
    Partially update a planet.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the planet to partially update.
    responses:
      200:
        description: Planet partially updated successfully.
      400:
        description: Bad request. Planet name is required.
      404:
        description: Planet not found.
    """
    planet_name = request.form.get('name')

    if not planet_name:
        return jsonify({"error": "Planet name is required"}), 400

    # Replace the following placeholder with your actual partial update logic
    # Example:
    # col.update_one({"name": planet_name}, {"$set": {"population": 1000000}})

    # Check if the planet was partially updated successfully and return the appropriate response


@app.route('/delete_planet', methods=['DELETE'])
def delete_planet():
    """
    Delete a planet.
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the planet to delete.
    responses:
      200:
        description: Planet deleted successfully.
      400:
        description: Bad request. Planet name is required.
      404:
        description: Planet not found.
    """
    planet_name = request.args.get('name')

    if not planet_name:
        return jsonify({"error": "Planet name is required"}), 400

    # Replace the following placeholder with your actual delete logic
    # Example:
    # col.delete_one({"name": planet_name})

    # Check if the planet was deleted successfully and return the appropriate response


if __name__ == '__main__':
    app.run(debug=True)