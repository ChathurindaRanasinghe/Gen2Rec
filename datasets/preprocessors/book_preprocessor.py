import csv
import json
import os

import requests

directory = 'data/books'
all_data = []


def extract_numeric_rating(rating_str):
    try:
        return float(rating_str.split()[0])
    except ValueError:
        return None


def replace_price_format(price):
    return price.replace(',', '')


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

with open(output_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

for row in rows:
    if row['Rating']:
        row['Rating'] = extract_numeric_rating(row['Rating'])
    if row['Price']:
        row['Price'] = replace_price_format(row['Price'])

for row in rows:
    if (not row['Category'] or not row['Title'] or not row['Author'] or not row['Type'] or not row['Rating']
            or not row['Price']):
        rows.remove(row)

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("CSV file has been successfully created.")
