import requests

url = "http://127.0.0.1:8000/users/"
data = {
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "2024-10-13",
  "email": "john.doe@example.com",
  "password": "strongpassword123",
  "phone_number": "555-1234",
  "competition": "First Competition",
  "agreed_to_rules": true
}

response = requests.post(url, json=data)
print(response.json())
