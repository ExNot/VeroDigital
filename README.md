# Vero Digital Python Task

This project consists of two Python scripts that share a common goal: downloading specific resources, merging them with CSV-transmitted resources, and converting them into a formatted Excel file.

## Installation

To set up and run this project, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Install the required packages: django, requests, pandas, openpyxl, restframework.
4. While inside the "veroServer" folder, start the server using the command: "python manage.py runserver." (The server-side code can be found in veroServer/api/views.py).
5. While inside the "veroClient" folder, run the program using the CLI with the following command: "python client.py -k {arguments} -c." The Excel file will be generated within the "veroClient" folder. You need to specify the column names you want to output after the -k argument (use -c if you want to color the Excel output).

## Contact

If you have any questions or feedback, please feel free to contact me at enesbaskale@gmail.com
