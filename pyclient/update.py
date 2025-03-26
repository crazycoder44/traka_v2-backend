import requests

endpoint = "http://localhost:8000/api/salestrakav2/users/1/update/"

data = {
    "id": 1,
    "lastname": "pondo",
    "address": "bucknor",
    "branchid": 1
}

get_response = requests.patch(endpoint, json=data)

print(get_response.json())

