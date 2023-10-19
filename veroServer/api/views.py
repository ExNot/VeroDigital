from rest_framework.response import Response
from rest_framework.decorators import  api_view
import requests

url = "https://api.baubuddy.de/index.php/login"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
access_token = data.get("oauth", {}).get("access_token")


url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
headers={
     "Authorization": f"Bearer {access_token}"
}
response = requests.get(url, headers=headers)
if response.status_code ==200:
    csv_data = response.text
    with open("output.csv", "w") as f:

        f.write(csv_data)
else:
    print("ERROR:", response.status_code)