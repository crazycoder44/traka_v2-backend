import requests

endpoint = "http://localhost:8000/api/salestrakav2/branches/1/"

#  Your authorization token (replace this with your actual token)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzg3NDI1LCJpYXQiOjE3NDIzODU2MjUsImp0aSI6ImFhZGUyOTU5OGRiNDQ3OWY4NDhjYTFlMjIyMDUxZjQ3IiwidXNlcl9pZCI6M30.Jrb7UVC82h-OSshPCphtaRXBKSeO7sVT89u-z7Tp9Rw"

# Define headers to include the token
headers = {
    "Authorization": f"Bearer {auth_token}"
}

get_response = requests.get(endpoint, headers=headers)

print(get_response.json())