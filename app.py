from flask import Flask, request, jsonify

app = Flask(__name__)

movies = []
next_id = 1

@app.route('/', methods=['GET'])
def api_overview():
    return jsonify({
        "available_endpoints": {
            "GET /movies": "List all movies",
            "GET /movies/<id>": "Get a movie by ID",
            "POST /movies": "Add a new movie",
            "PUT /movies/<id>": "Update a movie by ID",
            "DELETE /movies/<id>": "Delete a movie by ID"
        },
        "post_movie_format": {
            "title": "string",
            "year": "integer",
            "genre": "string"
        },
        "example": {
            "POST /movies": {
                "title": "Inception",
                "year": 2010,
                "genre": "Sci-Fi"
            }
        }
    })


@app.route('/movies', methods=['GET'])
def show_all_movies():
    return jsonify(movies)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def show_movie(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({'error': 'Movie not found'}), 404

@app.route('/movies', methods=['POST'])
def add_movie():
    global next_id
    data = request.get_json()
    movie = {
        'id': next_id,
        'title': data.get('title'),
        'year': data.get('year'),
        'genre': data.get('genre')
    }
    movies.append(movie)
    next_id += 1
    return jsonify(movie), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.get_json()
    for movie in movies:
        if movie['id'] == movie_id:
            movie['title'] = data.get('title', movie['title'])
            movie['year'] = data.get('year', movie['year'])
            movie['genre'] = data.get('genre', movie['genre'])
            return jsonify(movie)
    return jsonify({'error': 'Movie not found'}), 404

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global movies
    movies = [m for m in movies if m['id'] != movie_id]
    return jsonify({'message': 'Movie deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
