import sqlite3

DATABASE_NAME = 'users.db'

def initialize_db():
    """Creates the users table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email):
    """Adds a new user to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Handles UNIQUE constraint violation (e.g., username already exists)
        return False
    finally:
        conn.close()

def get_all_users():
    """Retrieves all users from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute('SELECT username, email FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

# Ensure the database and table are created when the app starts
initialize_db()