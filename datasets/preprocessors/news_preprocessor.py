import csv
import json

with open('News_Category_Dataset_v3.json', 'r') as json_file:
    json_data = json_file.readlines()

first_entry = json.loads(json_data[0])
field_names = list(first_entry.keys())

with open('../news_dataset.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(field_names)

    for line in json_data:
        data = json.loads(line)
        csv_row = [data[field] for field in field_names]
        writer.writerow(csv_row)

print("CSV file has been successfully created.")
