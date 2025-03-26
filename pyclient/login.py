import requests

endpoint = "http://localhost:8000/api/salestrakav2/login/"

data = {
    "email": "panda@gmail.com",
    "password": "1234567",
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())