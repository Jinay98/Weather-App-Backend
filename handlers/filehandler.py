import os

import xlsxwriter
from django.conf import settings


class FileHandler:
    def __init__(self, data):
        self.data = data
        self.file_path = os.path.join(settings.MEDIA_ROOT, "weather-report.xlsx")

    def clean_data(self):
        cleaned_data = []
        for item in self.data:
            row = []
            city_id = item.get("id", None)
            city_name = item.get("name", None)
            coord_lat = item["coord"]["lat"]
            coord_lon = item["coord"]["lon"]
            temp = item["main"]["temp"]
            feels_like = item["main"]["feels_like"]
            temp_min = item["main"]["temp_min"]
            temp_max = item["main"]["temp_max"]
            pressure = item["main"]["pressure"]
            humidity = item["main"]["humidity"]
            row.extend(
                (city_id, city_name, coord_lat, coord_lon, temp, feels_like, temp_min, temp_max, pressure, humidity))
            cleaned_data.append(row)

        return cleaned_data

    def create_excel_file(self):
        cleaned_data = self.clean_data()

        workbook = xlsxwriter.Workbook(self.file_path)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'ID')
        worksheet.write('B1', 'City')
        worksheet.write('C1', 'Latitude')
        worksheet.write('D1', 'Longitude')
        worksheet.write('E1', 'Temperature')
        worksheet.write('F1', 'Feels Like')
        worksheet.write('G1', 'Min Temp')
        worksheet.write('H1', 'Max Temp')
        worksheet.write('I1', 'Pressure')
        worksheet.write('J1', 'Humidity')

        row = 1
        col = 0

        for city_id, city_name, coord_lat, coord_lon, temp, feels_like, temp_min, temp_max, pressure, humidity in (
                cleaned_data):
            worksheet.write(row, col, city_id)
            worksheet.write(row, col + 1, city_name)
            worksheet.write(row, col + 2, coord_lat)
            worksheet.write(row, col + 3, coord_lon)
            worksheet.write(row, col + 4, temp)
            worksheet.write(row, col + 5, feels_like)
            worksheet.write(row, col + 6, temp_min)
            worksheet.write(row, col + 7, temp_max)
            worksheet.write(row, col + 8, pressure)
            worksheet.write(row, col + 9, humidity)
            row += 1

        workbook.close()

    def delete_excel_file(self):
        if os.path.isfile(self.file_path):
            print("File exist")
            os.remove(self.file_path)
