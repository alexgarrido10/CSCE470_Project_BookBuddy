from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

# app instance 
app = Flask(__name__)
CORS(app)

# /api/home

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Hello World from College Station"
    })

@app.route("/api/search", methods=['GET'])
def search_books():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    
    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400
    
    # Call BM25 script and pass the query to it
    try:
        result = subprocess.run(
            ['python3.12', 'bm25.py', query],  # Run bm25.py with the query
            capture_output=True, text=True
        )
        # Capture the output and send it as JSON
        output = result.stdout.splitlines()
        top_books = [{"rank": i+1, "title": line.split(' - ')[0], "score": line.split(':')[1]} for i, line in enumerate(output)]
        
        return jsonify(top_books)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8080)

