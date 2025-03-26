import requests

endpoint = "http://localhost:8000/api/salestrakav2/branches/"


# Your authorization token (replace this with your actual token)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzk1NjQ4LCJpYXQiOjE3NDIzOTM4NDgsImp0aSI6IjlmZTBlODE5Yjk2MzQxZGU4MzE1OTNhYjQ2ZjA3YTk1IiwidXNlcl9pZCI6M30.Vj_rrsZD5ux2X1kIEh9YNOmvLM45Jv1--u2mV-8LvWA"

# Define headers to include the token
headers = {
    "Authorization": f"Bearer {auth_token}"
}

# Make the GET request with the authorization token
get_response = requests.get(endpoint, headers=headers)

print(get_response.json())