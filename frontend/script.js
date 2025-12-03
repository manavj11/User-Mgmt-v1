document.addEventListener('DOMContentLoaded', () => {
    // Attach event listener to the form
    document.getElementById('user-form').addEventListener('submit', handleCreateUser);
    
    // Initial fetch to display existing users
    fetchAndDisplayUsers();
});

// --- 1. Hardcoded Secret Key (Demonstration Only!) ---
// NOTE: This must match the SECRET_API_KEY in backend/app.py
const API_TOKEN = "super-secure-dev-key-12345";
const API_URL = '/api/users';

const messageElement = document.getElementById('message');

function showMessage(text, isError = false) {
    messageElement.textContent = text;
    messageElement.className = isError ? 'error' : 'success';
    messageElement.classList.remove('hidden');
    setTimeout(() => messageElement.classList.add('hidden'), 5000);
}

// --- 2. Function to Create User ---
async function handleCreateUser(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    if (!username || !email) {
        showMessage("Please fill in both fields.", true);
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // --- Key Showcase: Basic Token Transfer in the Authorization Header ---
                'Authorization': `Bearer ${API_TOKEN}` 
            },
            body: JSON.stringify({ username, email })
        });

        const result = await response.json();
        
        if (response.ok) {
            showMessage(result.message, false);
            // Clear form and update list
            document.getElementById('user-form').reset();
            fetchAndDisplayUsers();
        } else {
            // Handle 401 (Unauthorized) or 409 (Conflict)
            showMessage(`Error: ${result.message}`, true);
        }

    } catch (error) {
        console.error('Network or server error:', error);
        showMessage('A network error occurred. Check the server.', true);
    }
}

// --- 3. Function to Fetch and Display Users ---
async function fetchAndDisplayUsers() {
    const userListElement = document.getElementById('user-list');
    userListElement.innerHTML = '<li>Loading users...</li>'; // Clear and set loading message

    try {
        const response = await fetch(API_URL, {
            method: 'GET',
            headers: {
                // --- The token is sent for the GET request as well for validation ---
                'Authorization': `Bearer ${API_TOKEN}` 
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            userListElement.innerHTML = `<li class="error">${errorData.message}</li>`;
            return;
        }

        const users = await response.json();
        
        // Clear list and display users
        userListElement.innerHTML = '';
        if (users.length === 0) {
            userListElement.innerHTML = '<li>No users registered yet.</li>';
        } else {
            users.forEach(user => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${user.username}</strong> <span>(${user.email})</span>`;
                userListElement.appendChild(li);
            });
        }

    } catch (error) {
        console.error('Fetch error:', error);
        userListElement.innerHTML = '<li class="error">Failed to load users. Check console.</li>';
    }
}