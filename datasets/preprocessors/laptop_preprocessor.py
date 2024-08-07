import json
from datetime import datetime

import pandas as pd


def read_data(json_file):
    with open(json_file, "r") as file:
        return json.load(file)


def remove_duplicates(data):
    seen = set()
    unique_data = []
    for item in data:
        model_info = item["model_info"][0]
        identifier = (model_info["name"], model_info["extra_name"], tuple(model_info["submodel_info"]))
        if identifier not in seen:
            seen.add(identifier)
            unique_data.append(item)
    return unique_data


def process_json(data):
    if isinstance(data, dict):
        return {k: process_json(v) for k, v in data.items() if v is not None and v != ""}
    elif isinstance(data, list):
        return [process_json(item) for item in data]
    elif isinstance(data, str):
        try:
            return float(data)
        except ValueError:
            return data
    else:
        return data


def create_new_dataset(data):
    new_dataset = []
    for item in data:
        try:
            new_item = {
                "name": item["model_info"][0]["name"],
                "thumbnail": item["model_resources"]["thumbnail"],
                "launch_year": datetime.strptime(item["model_resources"]["launch_date"], "%Y-%m-%d").year,
                "cpu": process_json(item["cpu"]),
                "gpu": process_json(item["gpu"]),
                "display": process_json(item["display"]),
                "memory": process_json(item["memory"]),
                "primary_storage": process_json(item["primary_storage"]),
                "secondary_storage": process_json(item["secondary_storage"]),
                "total_storage_capacity": process_json(item["total_storage_capacity"]),
                "wireless_card": process_json(item["wireless_card"]),
                "motherboard": process_json(item["motherboard"]),
                "chassis": process_json(item["chassis"]),
                "battery": process_json(item["battery"]),
                "battery_life_hours": sum(
                    float(x) / 60 ** i for i, x in enumerate(item["battery_life_hours"].split(":"))),
                "operating_system": process_json(item["operating_system"]),
                "warranty": process_json(item["warranty"]),
                "price": process_json(item["config_price"]),
            }
            new_dataset.append(new_item)
        except:
            print(f"Failed to process {item['model_info'][0]['name']}")

    return new_dataset


def flatten_data(y):
    out = pd.json_normalize(data=y, sep="_", max_level=1)
    return out


def save_to_file(processed_data, output_file):
    processed_data.to_csv(output_file, sep=',', encoding='utf-8')


if __name__ == "__main__":
    input_file = "data/collected_data.json"
    output_file = "data/laptop_dataset.csv"

    cleaned_data = remove_duplicates(read_data(input_file))
    processed_data = create_new_dataset(cleaned_data)
    flatten_data = flatten_data(processed_data)
    save_to_file(flatten_data, output_file)

    print("CSV file has been successfully created.")
