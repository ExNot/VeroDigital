from rest_framework.response import Response
from rest_framework.decorators import api_view
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
headers = {
    "Authorization": f"Bearer {access_token}"
}
print(access_token)
response = requests.get(url, headers=headers)
if response.status_code == 200:

    json_data = response.json()

    csv_data = pd.read_csv('vehicles.csv', sep=';')
    json_data_df = pd.DataFrame(json_data)

    merged_df = csv_data.merge(json_data_df, on='kurzname', how='outer')

    merged_df['labelIds_x'] = merged_df['labelIds_x'].astype(str)
    merged_df['labelIds_y'] = merged_df['labelIds_y'].astype(str)


    merged_df['gruppe_x'].fillna(merged_df['gruppe_y'], inplace=True)
    merged_df['langtext_x'].fillna(merged_df['langtext_y'], inplace=True)
    merged_df['info_x'].fillna(merged_df['info_y'], inplace=True)
    merged_df['lagerort_x'].fillna(merged_df['lagerort_y'], inplace=True)
    merged_df['labelIds_x'].fillna(merged_df['labelIds_y'], inplace=True)

    merged_df = merged_df.drop(['gruppe_y', 'langtext_y', 'info_y', 'lagerort_y', 'labelIds_y'], axis=1)
    merged_df.columns = merged_df.columns.str.rstrip('_x')

    hu_filtered_df = merged_df[merged_df['hu'].notna()]

    hu_filtered_df = hu_filtered_df.where(pd.notna(hu_filtered_df), None)
    hu_filtered_df = hu_filtered_df.to_dict(orient='records')
    with open('filtered_data.json', 'w', encoding="utf-8") as merged_json_file:
        json.dump(hu_filtered_df, merged_json_file, ensure_ascii=False, indent=4)





else:
    print("ERROR:", response.status_code)
