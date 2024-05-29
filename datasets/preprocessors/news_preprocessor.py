import csv
import json


def convert_json_to_csv(input_file, output_file):
    with open(input_file, "r") as json_file:
        json_data = json_file.readlines()

    first_entry = json.loads(json_data[0])
    field_names = list(first_entry.keys())

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(field_names)

        for line in json_data:
            data = json.loads(line)
            csv_row = [data[field] for field in field_names]
            writer.writerow(csv_row)


if __name__ == "__main__":
    input_file = "data/News_Category_Dataset_v3.json"
    output_file = "data/news_dataset.csv"

    convert_json_to_csv(input_file, output_file)

    print("CSV file has been successfully created.")
