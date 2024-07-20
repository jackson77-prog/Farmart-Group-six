from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load the animal data from the JSON file
with open('animals.json', 'r') as f:
    animals = json.load(f)

# Endpoint to get all animals
@app.route('/api/animals', methods=['GET'])
def get_animals():
    return jsonify({'animals': animals})

# Endpoint to get a specific animal by ID
@app.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    animal = next((animal for animal in animals if animal['id'] == animal_id), None)
    if animal:
        return jsonify(animal)
    else:
        return jsonify({'error': 'Animal not found'}), 404

# Endpoint to add a new animal
@app.route('/api/animals', methods=['POST'])
def add_animal():
    new_animal = request.json
    new_animal['id'] = len(animals) + 1  # Simple ID generation
    animals.append(new_animal)
    return jsonify(new_animal), 201

# Endpoint to update an animal's details
@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    animal = next((animal for animal in animals if animal['id'] == animal_id), None)
    if animal:
        data = request.json
        animal.update(data)
        return jsonify(animal)
    else:
        return jsonify({'error': 'Animal not found'}), 404

# Endpoint to delete an animal
@app.route('/api/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    global animals
    animals = [animal for animal in animals if animal['id'] != animal_id]
    return jsonify({'message': 'Animal deleted'})

if __name__ == '__main__':
    app.run(debug=True)

