import pandas as pd


def preprocess_and_save(input_file, output_file):
    df = pd.read_csv(input_file)

    purchased_data = df[df['Purchased or Played'] == 'purchase']
    played_data = df[df['Purchased or Played'] == 'play']

    user_purchased_games = {}
    user_played_games = {}

    for _, row in purchased_data.iterrows():
        user_id = row['User ID']
        game_name = row['Game Name']
        if user_id not in user_purchased_games:
            user_purchased_games[user_id] = [game_name]
        else:
            user_purchased_games[user_id].append(game_name)

    for _, row in played_data.iterrows():
        user_id = row['User ID']
        game_name = row['Game Name']
        if user_id not in user_played_games:
            user_played_games[user_id] = [game_name]
        else:
            user_played_games[user_id].append(game_name)

    purchased_count = purchased_data.groupby('Game Name').size().reset_index(name='Purchased Count')
    play_hours = played_data.groupby('Game Name')[
        'Hours if behavior is play, 1.0 if behavior is purchase'].sum().reset_index()
    gamewise_data = pd.merge(purchased_count, play_hours, on='Game Name', how='outer').fillna(0)

    gamewise_data.rename(columns={'Hours if behavior is play, 1.0 if behavior is purchase': 'Hours Played'},
                         inplace=True)
    gamewise_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    input_file = "data/steam-200k.csv"
    output_file = "data/game_dataset.csv"

    preprocess_and_save(input_file, output_file)

    print("CSV file has been successfully created.")
