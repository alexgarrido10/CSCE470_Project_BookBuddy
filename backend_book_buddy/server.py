from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

# app instance 
app = Flask(__name__)
CORS(app)

# /api/home
# was for testing website
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Hello World from College Station"
    })


#for the search query connection to bm25
@app.route("/api/search", methods=['GET'])
def search_books():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    mood = request.args.get('mood', None)  # Get the 'mood' parameter from the URL, none if nothing is given

    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400
    
    # command
    command = ['python3.12', 'bm25.py', query]
    # only incorporate mood if needed
    if mood:
        command.extend(['-s', mood])

    # Call BM25 script and pass the query to it
    try:
        result = subprocess.run(
            command,  # pass command
            capture_output=True, text=True
        )
        # error
        if result.returncode != 0:
            return jsonify({'error': 'BM25 script failed', 'details': result.stderr}), 500

        # Parse the output
        output = result.stdout.splitlines()
        top_books = [{"rank": i + 1, "title": line.split(' - ')[0], "score": line.split(':')[1]} for i, line in enumerate(output)]

        return jsonify(top_books)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=8080)

