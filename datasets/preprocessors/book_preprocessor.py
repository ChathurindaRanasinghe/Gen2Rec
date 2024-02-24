import csv
import json
import os

import requests

directory = 'data/books'
all_data = []

if os.path.exists('genres.csv'):
    os.remove('genres.csv')

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        category = os.path.splitext(filename)[0]
        with open(filepath, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            header_row = next(reader)
            data = [[category] + row for row in reader]
            all_data.extend(data)

for d in all_data:
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={d[1].replace(' ', '%20')}")
        data = json.loads(response.text)
        items = data["items"]
        for item in items:
            description = item["volumeInfo"]["description"]
            d.append(description)
            print(f"found for {d[1]}")
            break
    except:
        print(f"not found for {d[1]}")
        all_data.remove(d)

output_file = '../book_dataset.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Category'] + ['Title'] + ['Author'] + ['Type'] + ['Rating'] + ['Price'] + ['Description'])
    writer.writerows(all_data)

print("CSV file has been successfully created.")
