import json

import pandas as pd


def process_data(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    flattened_data = []
    for entry in json_data:
        if entry is not None:
            flattened_entry = {
                "name": entry.get("name", ""),
                "price": entry.get("price", "").replace("$", "").replace(",", "").strip(),
                "features": ", ".join(entry.get("features", [])),
                "history": ", ".join(entry.get("history", [])),
                "seller_notes": entry.get("seller_notes", ""),
                "seller": entry.get("seller", ""),
                "review": entry.get("review", "")
            }

            overview_mapping = {
                "mileage": "",
                "doors": "",
                "transmission": "",
                "engine": "",
                "drivetrain": ""
            }
            for item in entry.get("overview", []):
                if "miles" in item.lower():
                    overview_mapping["mileage"] = item.replace("miles", "").replace(",", "").strip()
                elif "doors" in item.lower():
                    overview_mapping["doors"] = item.replace("Doors", "").strip()
                elif "transmission" in item.lower():
                    overview_mapping["transmission"] = item
                elif "cylinder" in item.lower():
                    overview_mapping["engine"] = item
                elif "drive" in item.lower():
                    overview_mapping["drivetrain"] = item

            if len(entry.get("overview", [])) > 6:
                overview_mapping["interior_color"] = entry.get("overview", [])[1]
                overview_mapping["exterior_color"] = entry.get("overview", [])[2]

            flattened_entry.update(overview_mapping)
            flattened_data.append(flattened_entry)
    return flattened_data


def save_to_csv(flattened_data, output_file):
    df = pd.DataFrame(flattened_data)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    input_file = "data/scraped_data.json"
    output_file = "data/vehicle_dataset.csv"

    flattened_data = process_data(input_file)
    save_to_csv(flattened_data, output_file)

    print("CSV file has been successfully created.")
