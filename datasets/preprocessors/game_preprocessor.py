import csv
import json


def preprocess_and_create_json(filename):
    data = {}

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row['User ID']
            game_name = row['Game Name']
            behavior = row['Purchased or Played']
            hours = float(row['Hours if behavior is play, 1.0 if behavior is purchase'])

            if user_id not in data:
                data[user_id] = {'played_games': {}, 'purchased_games': []}

            if behavior == 'play':
                if game_name in data[user_id]['played_games']:
                    data[user_id]['played_games'][game_name] += hours
                else:
                    data[user_id]['played_games'][game_name] = hours
            elif behavior == 'purchase':
                data[user_id]['purchased_games'].append(game_name)

    return data


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


csv_file = 'data/steam-200k.csv'
output_file = '../game_dataset.json'

player_data = preprocess_and_create_json(csv_file)
write_json_to_file(player_data, output_file)
print("JSON file has been successfully created.")
