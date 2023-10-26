import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.workbook import Workbook

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
with open('vehicles.csv', 'r', encoding='utf-8') as csv_file:
    csv_data = csv_file.read()
data = {'csv_file': ('vehicles.csv', csv_data)}
url = "http://127.0.0.1:8000/api/upload_csv/"
response = requests.post(url, files=data)
if response.status_code == 200:
    print('CSV dosyası başarıyla sunucuya yüklendi.')
else:
    print('CSV dosyası yükleme hatası:', response.status_code)

colored = True

def calculate_color_code_hu(hu):
    today = datetime.now()

    if hu is None:
        return None

    hu_date = datetime.strptime(hu, "%Y-%m-%d")

    if hu_date > today:
        return None

    date_gap = today-hu_date

    if date_gap.days <90:
        return "#007500"
    elif 90<= date_gap.days <365:
        return "#FFA500"
    else:
        return "#b30000"




with open('filtered_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)

#data = df.sort_values(by='gruppe')
data = df.sort_values(by='gruppe')

wb = Workbook()
ws = wb.active

header = data.columns.tolist()
ws.append(header)

fill_green = PatternFill(start_color="007500", end_color="007500", fill_type="solid")
fill_orange = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
fill_red = PatternFill(start_color="b30000", end_color="b30000", fill_type="solid")

for _, row in data.iterrows():
    row_data = [row[column] for column in header]
    ws.append(row_data)

    color_code = calculate_color_code_hu(row['hu'])
    if color_code == "#007500":
        for row in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col=len(header)):
            for cell in row:
                cell.fill = fill_green
    elif color_code == "#FFA500":
        for row in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col=len(header)):
            for cell in row:
                cell.fill = fill_orange
    elif color_code == "#b30000":
        for row in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col=len(header)):
            for cell in row:
                cell.fill = fill_red


wb.save('colored_vehicles.xlsx')





















