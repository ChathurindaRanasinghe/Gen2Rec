import csv
import json

with open("data/scraped_data.json", 'r', encoding='utf-8') as f:
    json_data = json.load(f)

csv_columns = ["name", "price", "overview", "features", "history", "seller_notes", "seller", "review"]

flattened_data = []
for entry in json_data:
    if entry is not None:
        flattened_entry = {
            "name": entry.get("name", ""),
            "price": entry.get("price", ""),
            "overview": ", ".join(entry.get("overview", [])),
            "features": ", ".join(entry.get("features", [])),
            "history": ", ".join(entry.get("history", [])),
            "seller_notes": entry.get("seller_notes", ""),
            "seller": entry.get("seller", ""),
            "review": entry.get("review", "")
        }
        flattened_data.append(flattened_entry)

with open("../vehicle_dataset.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()
    for data in flattened_data:
        writer.writerow(data)

print("CSV file has been successfully created.")
