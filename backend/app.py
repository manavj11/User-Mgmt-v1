# from flask import Flask, request, jsonify, send_from_directory
from flask import Flask, request, jsonify, send_from_directory, session
import database
import os


app = Flask(__name__, static_folder='../frontend', static_url_path='')

# --- 1. Hardcoded Secret for Basic Auth ---
# !!! DEMONSTRATION ONLY. Use environment variables in production.
# SECRET_API_KEY = "super-secure-dev-key-12345"

# 1. DELETE the hardcoded SECRET_API_KEY and the is_authenticated function.
# 2. ADD a SECURE SECRET_KEY for session management.
# In a real app, this should be a long random string loaded from an environment variable.
app.config['SECRET_KEY'] = 'a-much-longer-and-more-random-session-secret-9876'


# # --- 2. Authentication Helper Function ---
# def is_authenticated(req):
#     """Checks for the presence and validity of the secret key in the request's Authorization header."""
#     auth_header = req.headers.get('Authorization')
#     expected_header = f'Bearer {SECRET_API_KEY}'
    
#     if auth_header and auth_header == expected_header:
#         return True
#     return False


# --- 2. New: A Simple Placeholder "Login" Endpoint ---
# This simulates how a real user would establish a session.
@app.route('/api/login', methods=['POST'])
def login():
    # Security Note: This is a placeholder for actual login logic!
    # A real application would check username/password here.
    
    # For this demonstration, we'll just establish a session immediately.
    # We set a value in the session object to mark the user as authenticated.
    session['user_id'] = 'admin' 
    
    return jsonify({"message": "Session established successfully."}), 200


# --- 2.5. New: Authentication Helper for Session Check ---
# Replaces the old is_authenticated function.
def is_authenticated_by_session():
    """Checks if a session value (e.g., 'user_id') exists."""
    is_auth = 'user_id' in session
    print(f"DEBUG: Session check for 'user_id' returned: {is_auth}")
    return is_auth


# --- 3. User Creation (POST) Endpoint ---
@app.route('/api/users', methods=['POST'])
def create_user():
    # # Enforce Auth Token Transfer
    # if not is_authenticated(request):
    #     return jsonify({"message": "Authentication required. Missing or invalid Bearer token."}), 401

    # Enforce Session Check
    if not is_authenticated_by_session():
        # Redirect the client if they are not logged in (session not established)
        return jsonify({"message": "Unauthorized. Please log in to establish a session."}), 401

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
    # # Enforce Auth Token Transfer
    # if not is_authenticated(request):
    #     return jsonify({"message": "Authentication required. Missing or invalid Bearer token."}), 401

    # Enforce Session Check
    if not is_authenticated_by_session():
        return jsonify({"message": "Unauthorized. Please log in to establish a session."}), 401

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