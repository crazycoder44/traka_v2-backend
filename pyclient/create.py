import requests

endpoint = "http://localhost:8000/api/salestrakav2/register/"

data = {
    "firstname": "panda",
    "lastname": "hyena",
    "gender": "Male",
    "email": "panda@gmail.com",
    "mobile": "9126751245",
    "address": "nepa",
    "role": "Sales Rep",
    "branchid": 1,
}

# Your authorization token (replace this with your actual token)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNTc1OTg3LCJpYXQiOjE3NDI1NzQxODcsImp0aSI6ImFhMTJiNWE0M2JiMjRmMWNiYjY2NDgxZWE4NmI5MDAzIiwidXNlcl9pZCI6MX0.wal18DnPHpaw4RG97r0rGV680CJf_koo3YgILfKvngo"

# Define headers to include the token
headers = {
    "Authorization": f"Bearer {auth_token}"
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())

# data = {
#     "email": "panda@gmail.com",
#     "password": "1234567"
# }

# data = {
#     "orderid": "652fa563dce245",
#     "productid": 2,
#     "quantity": 1,
#     "action": "Replace",
#     "userid": 1,
#     "branchid": 1
# }

# data = [
#     {
#     "ordersrc": "Instagram",
#     "productid": 1,
#     "quantity": 1,
#     "unit_price": 127000.00,
#     "userid": 1,
#     "branchid": 1,
#     "payment_choice": "Cash",
# }
# ]

# data = {
#     "productid": 3,
#     "userid": 1,
#     "branchid": 3,
#     "quantity": 20
# }

# data = {
#     "firstname": "panda",
#     "lastname": "hyena",
#     "gender": "Male",
#     "email": "babaitu@gmail.com",
#     "mobile": "9126751245",
#     "address": "nepa",
#     "role": "Sales Rep",
#     "branchid": 1,
# }

# data = {
#     "productname": "Air Fryer",
#     "price": 127000.00
# }

# data = {
#     "branchname": "oshodi",
#     "address": "gbera",
#     "mobile": 9023416389
# }

# data = {
#     "firstname": "lamba",
#     "lastname": "waybad",
#     "gender": "Male",
#     "email": "lamba@gmail.com",
#     "mobile": 9011002000,
#     "address": "gbafuo",
#     "role": "Sales Rep",
#     "branchid": 2
# }