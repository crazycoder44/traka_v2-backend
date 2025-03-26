import requests

endpoint = "http://localhost:8000/api/salestrakav2/returns/1/delete/"


get_response = requests.delete(endpoint)

print(get_response)