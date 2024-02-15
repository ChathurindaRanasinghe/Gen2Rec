import csv
import os

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

output_file = '../book_dataset.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Category'] + ['Title'] + ['Author'] + ['Type'] + ['Rating'] + ['Price'])
    writer.writerows(all_data)

print("CSV file has been successfully created.")
