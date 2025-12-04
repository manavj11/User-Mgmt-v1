# 🔒 Auth & User Management App (user-mgmt-v1)

This project is a minimal full-stack application designed to showcase a fundamental user flow for SaaS Apps: **Data Storage** and **authenticated API calls** using a **Bearer Token**.

The backend is built with Python (Flask) and SQLite, and the frontend is a simple HTML/CSS/JavaScript interface.

## 🚀 Project Structure

user-mgmt-v1/ ├── .gitignore # Files to ignore for Git ├── README.md # This file ├── requirements.txt # Python dependencies (Flask) ├── backend/ │ ├── app.py # Flask application, API endpoints, and authentication logic │ ├── database.py # SQLite database initialization and CRUD operations │ └── users.db # Automatically generated SQLite database file └── frontend/ ├── index.html # User Creation form and User List display ├── style.css # Basic styling └── script.js # Frontend logic, including the hardcoded API token

## ✨ Key Features Demonstrated

1.  **Basic Token Authentication:** The frontend sends a hardcoded `Bearer super-secure-dev-key-12345` token with every request.
2.  **Backend Token Validation:** The `backend/app.py` file checks for this exact token before processing any request.
3.  **Full-Stack Flow:** Seamless creation and retrieval of user data between the browser, Flask API, and SQLite database.

## 🛠️ How to Run the Project

### Prerequisites

* **Python 3.6+**
* **pip** (Python package installer)

### Step 1: Clone the Repository

*(Assuming you have already created the project folders and files as discussed.)*

### Step 2: Install Python Dependencies

1.  Navigate to the root directory of the project (`user-mgmt-v1`).
2.  Install the necessary packages using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Run the Backend Server

1.  Navigate into the `backend` directory:

    ```bash
    cd backend
    ```

2.  Run the Flask application:

    ```bash
    python app.py
    ```

    You should see output indicating the server is running, typically at `http://127.0.0.1:5000/`.

### Step 4: Access the Frontend

1.  Open your web browser.
2.  Navigate to the server address: `http://127.0.0.1:5000/`
3.  The backend serves the `frontend/index.html` file by default (via the root route `/` in `app.py`).

You can now use the form to create new users and see them appear in the list below. The user list will only load if the correct token is sent with the GET request.

---

## 🗑️ .gitignore Content

This is a standard set of exclusions for a Python/Flask project to keep the repository clean.
