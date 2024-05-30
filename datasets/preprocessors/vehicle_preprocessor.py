import csv
import json


def process_data(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    flattened_data = []
    for entry in json_data:
        if entry is not None:
            flattened_entry = {
                "name": entry.get("name", ""),
                "price": entry.get("price", "").replace("$", "").replace(",", "").strip(),
                "overview": ", ".join(entry.get("overview", [])),
                "features": ", ".join(entry.get("features", [])),
                "history": ", ".join(entry.get("history", [])),
                "seller_notes": entry.get("seller_notes", ""),
                "seller": entry.get("seller", ""),
                "review": entry.get("review", "")
            }
            flattened_data.append(flattened_entry)
    return flattened_data


def save_to_csv(flattened_data, output_file):
    csv_columns = ["name", "price", "overview", "features", "history", "seller_notes", "seller", "review"]
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for data in flattened_data:
            writer.writerow(data)


if __name__ == "__main__":
    input_file = "data/scraped_data.json"
    output_file = "data/vehicle_dataset.csv"

    flattened_data = process_data(input_file)
    save_to_csv(flattened_data, output_file)

    print("CSV file has been successfully created.")
