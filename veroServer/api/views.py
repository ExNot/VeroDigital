from rest_framework.response import Response
from rest_framework.decorators import  api_view
import requests
import json
import pandas as pd

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

    json_data = response.json()
    with open("output.json", "w") as json_file:
        json.dump(json_data, json_file)

    with open('output.json', 'r', encoding="utf-8") as json_for_filter:
        data = json.load(json_for_filter)

    filtered_data = [item for item in data if item['hu'] is not None]

    with open('filtered_output.json', 'w', encoding="utf-8") as filtered_json_file:
        json.dump(filtered_data, filtered_json_file, indent=4, ensure_ascii=False)

else:
    print("ERROR:", response.status_code)
