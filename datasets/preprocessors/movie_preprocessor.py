import csv

import pandas as pd
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


def fetch_data(movies):
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


def flatten_and_clean_data(data):
    fields_to_remove = ["Type","DVD","Production", "Website"]
    flat_data = []
    for item in data:
        flat_item = {
            "Title": item.get("Title"),
            "Year": item.get("Year"),
            "Rated": item.get("Rated"),
            "Released": item.get("Released"),
            "Runtime": item.get("Runtime"),
            "Genre": item.get("Genre"),
            "Director": item.get("Director"),
            "Writer": item.get("Writer"),
            "Actors": item.get("Actors"),
            "Plot": item.get("Plot"),
            "Language": item.get("Language"),
            "Country": item.get("Country"),
            "Awards": item.get("Awards"),
            "Poster": item.get("Poster"),
            "Metascore": item.get("Metascore"),
            "imdbRating": item.get("imdbRating"),
            "imdbVotes": item.get("imdbVotes"),
            "imdbID": item.get("imdbID"),
            "Type": item.get("Type"),
            "DVD": item.get("DVD"),
            "BoxOffice": item.get("BoxOffice"),
            "Production": item.get("Production"),
            "Website": item.get("Website"),
        }
        if "Ratings" in item:
            for rating in item["Ratings"]:
                source = rating.get("Source")
                value = rating.get("Value")
                if source and value:
                    flat_item[f"Rating_{source}"] = value

        for field in fields_to_remove:
            if field in flat_item:
                del flat_item[field]

        flat_data.append(flat_item)
    return flat_data


def save_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    input_file = "data/movies.csv"
    output_file = "data/movie_dataset.csv"

    movies = get_data(input_file)
    dataset = fetch_data(movies)
    cleaned_data = flatten_and_clean_data(dataset)
    save_to_csv(cleaned_data, output_file)

    print("CSV file has been successfully created.")
