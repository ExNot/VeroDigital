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


