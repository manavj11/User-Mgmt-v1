from flask import Flask, request, jsonify, send_from_directory
import database
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# --- 1. Hardcoded Secret for Basic Auth ---
# !!! DEMONSTRATION ONLY. Use environment variables in production.
SECRET_API_KEY = "super-secure-dev-key-12345"

# --- 2. Authentication Helper Function ---
def is_authenticated(req):
    """Checks for the presence and validity of the secret key in the request's Authorization header."""
    auth_header = req.headers.get('Authorization')
    expected_header = f'Bearer {SECRET_API_KEY}'
    
    if auth_header and auth_header == expected_header:
        return True
    return False

# --- 3. User Creation (POST) Endpoint ---
@app.route('/api/users', methods=['POST'])
def create_user():
    # Enforce Auth Token Transfer
    if not is_authenticated(request):
        return jsonify({"message": "Authentication required. Missing or invalid Bearer token."}), 401

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"message": "Missing username or email"}), 400

    if database.add_user(username, email):
        return jsonify({"message": f"User '{username}' added successfully!"}), 201
    else:
        return jsonify({"message": f"User '{username}' already exists or an error occurred."}), 409

# --- 4. User Retrieval (GET) Endpoint ---
@app.route('/api/users', methods=['GET'])
def get_users():
    # Enforce Auth Token Transfer
    if not is_authenticated(request):
        return jsonify({"message": "Authentication required. Missing or invalid Bearer token."}), 401
        
    users = database.get_all_users()
    return jsonify(users), 200

# Serve index.html
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Fallback for any other static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Initialize the database file and table
    database.initialize_db()
    # Run the Flask app
    app.run(debug=True)