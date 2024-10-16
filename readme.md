# User Management System - FastAPI Backend

This is a FastAPI backend for user management. It allows you to register users, authenticate them via login, and retrieve a list of registered users.

## Table of Contents

- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Deploying the Application](#deploying-the-application)

---

## Installation

1. **Clone the repository:**
   
   First, clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-folder>


2. Set up a virtual environment:

It is recommended to use a virtual environment to manage dependencies. To create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install the required dependencies:

Install all the necessary Python packages from the requirements.txt file:

pip install -r requirements.txt

Database Setup
SQLite Configuration:

By default, this backend uses an SQLite database. Make sure that users.db is created automatically at runtime.

If you wish to use another database (e.g., PostgreSQL, MySQL), modify the database URL in database.py:

python
Copy code
DATABASE_URL = "sqlite:///./users.db"  # Update to your preferred database URL
Creating Tables:

On the first run, the application will automatically create all necessary tables as specified in the models (in models.py), using the SQLAlchemy Base.metadata.create_all() function.

Running the Application
To run the FastAPI server locally:

bash
Copy code
uvicorn app:app --reload
The server will be available at http://127.0.0.1:8000/.

The --reload flag automatically restarts the server when you make changes to your code.

API Endpoints
Here are the main API endpoints available in this backend:

Register a New User:

POST /users/register
Request body: JSON containing user details
Example:
json
Copy code
{
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1990-01-01",
  "email": "john.doe@example.com",
  "password": "strongpassword",
  "phone_number": "1234567890",
  "competition": "Competition Name",
  "agreed_to_rules": true
}
Response: User details (without password)
Login:

POST /users/login
Request body: JSON containing email and password
Example:
json
Copy code
{
  "email": "john.doe@example.com",
  "password": "strongpassword"
}
Response: Access token
Get All Registered Users:

GET /users/retrieve
Response: List of all registered users
Get All Registered Users (Debug):

GET /users/retrieve_debug
Response: List of all registered users, also prints debug info to the terminal
Health Check:

GET /
Response: Welcome message
Deploying the Application
Option 1: Deploy on Heroku
Install the Heroku CLI if not already installed:

bash
Copy code
curl https://cli-assets.heroku.com/install.sh | sh
Login to Heroku:

bash
Copy code
heroku login
Create a Heroku App:

bash
Copy code
heroku create my-fastapi-app
Deploy the App: Push your code to Heroku and run it:

bash
Copy code
git push heroku master
Option 2: Deploy on DigitalOcean
Create a DigitalOcean Droplet with Ubuntu or any Linux distro.
SSH into the Droplet and set up Python, virtual environment, and dependencies.
Run Uvicorn or configure the app to run using Gunicorn + Nginx for production.
Open necessary ports and set up firewalls.
Additional Notes
CORS: If your front-end is hosted on a different domain than the backend, ensure that CORS is properly configured. You can add this in app.py:

python
Copy code
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Database Migration: If you plan on using a more advanced database (like PostgreSQL or MySQL), consider using Alembic for database migrations.

`uvicorn app:app --reload`

Enter email for superuser: admin@keen360.com
Enter password for superuser: admin123