import csv
import json

import requests


def get_data(input_file):
    movies = []
    with open(input_file, mode="r", encoding="utf8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            title_parts = row["title"].rsplit(" (", 1)
            movies.append(title_parts[0])
    return movies


def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


def parse_specific_fields(data):
    try:
        data["Year"] = int(data["Year"])
        data["Runtime"] = int(data["Runtime"].replace(" min", ""))
        data["imdbRating"] = float(data["imdbRating"])
        data["imdbVotes"] = int(data["imdbVotes"].replace(",", ""))
        print(data)
        return data
    except:
        return None


def fetch_data():
    api_key = ""
    api_url = f"http://www.omdbapi.com/?apikey={api_key}&t="

    dataset = []
    for i in range(len(movies)):
        try:
            data = fetch_data_from_api(api_url + movies[i])
            parsed_data = parse_specific_fields(data)
            if parsed_data:
                dataset.append(parsed_data)
        except:
            ...
    return dataset


def save_data_to_json(data, filename):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving data to JSON file: {e}")


if __name__ == "__main__":
    input_file = "data/movies.csv"
    output_file = "data/movie_dataset.json"

    movies = get_data(input_file)
    dataset = fetch_data()
    save_data_to_json(dataset, output_file)

    print("JSON file has been successfully created.")
