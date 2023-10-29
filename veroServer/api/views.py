
import requests
import json
import pandas as pd
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
import warnings
from django.http import HttpResponse


#warnings.filterwarnings("ignore") #if wanna ignore the warning : A value is trying to be set on a copy of a slice from a DataFrame.Try using .loc[row_indexer,col_indexer] = value instead


def get_access_token():

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
    return access_token



print(get_access_token())



@csrf_exempt
def upload_vehicles(request):
    if request.method == 'POST':
        uploaded_file = request.POST.get('csv_data', '')

        csv_data = uploaded_file

        df = pd.read_csv(StringIO(csv_data), sep=';', header=None)
        header_row = df.iloc[0]
        df = df[1:]
        df.columns = header_row
        df = df.dropna(axis=1, how='all')
        csv_data = df


        if not csv_data.empty:
            url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
            headers = {
                "Authorization": f"Bearer {get_access_token()}"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                json_data = response.json()

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

                #hu_filtered_df.at[0, 'labelIds'] = 76
                hu_filtered_df['colorCode'] = None
                for column in hu_filtered_df.columns:
                    hu_filtered_df.loc[hu_filtered_df[column].isin(["nan", "", "NaN"]), column] = None

                for index, row in hu_filtered_df.iterrows():

                    label_id = row['labelIds']
                    if label_id is not None:
                        url = f'https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}'
                        headers = {
                            "Authorization": f"Bearer {get_access_token()}"
                        }
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:

                            label_data = response.json()
                            color_code = label_data[0]['colorCode']
                            color_code = str(color_code)
                            hu_filtered_df.at[index, 'colorCode'] = color_code

                        else:
                            print(f'Error: There is no true formatted colorCode: {label_id}')

                hu_filtered_df['colorCode'] = hu_filtered_df['colorCode'].apply(lambda x: None if pd.isna(x) else x)
                hu_filtered_df['profilePictureUrl'] = hu_filtered_df['profilePictureUrl'].apply(
                    lambda x: None if pd.isna(x) else x)
                hu_filtered_df['thumbPathUrl'] = hu_filtered_df['thumbPathUrl'].apply(
                    lambda x: None if pd.isna(x) else x)

                hu_filtered_df = hu_filtered_df.to_dict(orient='records')

            else:
                print("ERROR:", response.status_code)

            response = json.dumps(hu_filtered_df)

            return JsonResponse({'data': response}, safe=False)
        else:
            return JsonResponse({'error': 'CSV verisi eksik.'}, status=400)
    else:
        return JsonResponse({'error': 'Geçersiz istek methodu.'}, status=405)