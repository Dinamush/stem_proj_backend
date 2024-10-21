import requests

# API endpoint for user registration
url = "http://127.0.0.1:8000/users/register"

# User registration payload
payload = {
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-01-01",
    "email": "john.doe@example.com",
    "password": "strongpassword123",
    "phone_number": "1234567890",
    "competition": "ScienceFair2024",
    "agreed_to_rules": True,
    "team_signup": False,
    "team_members": [],
    "team_member_emails": []
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the raw response
print("Status Code:", response.status_code)
print("Response Text:", response.text)
