import requests

# API endpoint for user login
url = "http://127.0.0.1:8000/users/login"

# Login payload
payload = {
    "username": "john.doe@example.com",  # This is the email
    "password": "strongpassword123"
}

# Send the POST request for login
response = requests.post(url, data=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
