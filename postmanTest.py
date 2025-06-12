from flask import Flask, request, jsonify

app = Flask(__name__)

# Initially, we have some films
films = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "year": 2010},
    {"id": 2, "title": "The Matrix", "director": "The Wachowskis", "year": 1999},
    {"id": 3, "title": "Interstellar", "director": "Christopher Nolan", "year": 2014}
]

# List all films (optional filtering by year, director, or id)
@app.route('/films', methods=['GET'])
def get_films():
    year = request.args.get('year')
    director = request.args.get('director')
    film_id = request.args.get('id')

    filtered_films = films

    if film_id:
        filtered_films = [f for f in filtered_films if str(f['id']) == film_id]

    if year:
        filtered_films = [f for f in filtered_films if str(f['year']) == year]

    if director:
        filtered_films = [f for f in filtered_films if director.lower() in f['director'].lower()]

    return jsonify(filtered_films)

# Add a new film
@app.route('/films', methods=['POST'])
def add_film():
    new_film = request.json
    films.append(new_film)
    return jsonify({"message": "Film added", "film": new_film}), 201

# Get a film by ID
@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = next((f for f in films if f["id"] == film_id), None)
    if film:
        return jsonify(film)
    return jsonify({"message": "Film not found"}), 404

# Update a film
@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = next((f for f in films if f["id"] == film_id), None)
    if film:
        data = request.json
        film.update(data)
        return jsonify({"message": "Film updated", "film": film})
    return jsonify({"message": "Film not found"}), 404

# Delete a film
@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    global films
    films = [f for f in films if f["id"] != film_id]
    return jsonify({"message": "Film deleted"})

if __name__ == '__main__':
    app.run(debug=True)
