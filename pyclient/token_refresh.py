import requests

# Your refresh token
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTkyMTgyMSwiaWF0IjoxNzQxODc4NjIxLCJqdGkiOiJkNTY2YTRjMzk2ZGU0N2NiODY4NTQ4ODUyYjQ5YmMzMCIsInVzZXJfaWQiOjF9.mkm5kqhOaaTJDznex07hT0sm1wxJuX582luNAjqphNI"

# The endpoint where the refresh token will be sent
endpoint = "http://localhost:8000/api/salestrakav2/token/refresh/"

# Sending a POST request with the refresh token
response = requests.post(endpoint, data={"refresh": refresh_token})

# Print the response (which should contain the new access token)
print(response.json())