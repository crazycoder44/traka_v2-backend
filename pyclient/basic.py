import requests

endpoint = "http://localhost:8000/"

get_response = requests.get(endpoint, json={"query": "Hello world"})

print(get_response.json())