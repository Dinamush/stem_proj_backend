import requests

# Step 1: Log in as superuser
login_url = "http://127.0.0.1:8000/users/login"
retrieve_users_url = "http://127.0.0.1:8000/users/retrieve_debug"

# Superuser credentials
superuser_credentials = {
    "username": "superuser@example.com",  # Replace with your superuser email
    "password": "superpassword123"        # Replace with your superuser password
}

# Log in and get the access token
login_response = requests.post(login_url, data=superuser_credentials)

# Check if login was successful
if login_response.status_code == 200:
    login_data = login_response.json()
    access_token = login_data['access_token']
    print("Superuser logged in successfully.")
    print(f"Access Token: {access_token}")
else:
    print("Superuser login failed.")
    print(f"Status Code: {login_response.status_code}")
    print(f"Response: {login_response.text}")
    exit()

# Step 2: Retrieve all users
# Set the headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Send GET request to retrieve all users
retrieve_response = requests.get(retrieve_users_url, headers=headers)

# Check if the request to retrieve users was successful
if retrieve_response.status_code == 200:
    users_data = retrieve_response.json()
    print("Retrieved users successfully.")
    print(f"Users: {users_data}")
else:
    print("Failed to retrieve users.")
    print(f"Status Code: {retrieve_response.status_code}")
    print(f"Response: {retrieve_response.text}")
