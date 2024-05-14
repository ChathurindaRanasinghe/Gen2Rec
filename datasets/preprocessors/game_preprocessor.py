import pandas as pd

df = pd.read_csv("data/steam-200k.csv")

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

userwise_data = pd.DataFrame(columns=['User ID', 'Purchased Games', 'Played Games'])

for user_id in set(list(user_purchased_games.keys()) + list(user_played_games.keys())):
    purchased_games = ', '.join(user_purchased_games.get(user_id, []))
    played_games = ', '.join(user_played_games.get(user_id, []))
    userwise_data = userwise_data._append(
        {'User ID': user_id, 'Purchased Games': purchased_games, 'Played Games': played_games}, ignore_index=True)

userwise_data.to_csv("../game_dataset(userwise).csv", index=False)
print("CSV file has been successfully created.")

purchased_count = purchased_data.groupby('Game Name').size().reset_index(name='Purchased Count')
play_hours = played_data.groupby('Game Name')[
    'Hours if behavior is play, 1.0 if behavior is purchase'].sum().reset_index()
gamewise_data = pd.merge(purchased_count, play_hours, on='Game Name', how='outer').fillna(0)

gamewise_data.rename(columns={'Hours if behavior is play, 1.0 if behavior is purchase': 'Hours Played'}, inplace=True)
gamewise_data.to_csv("../game_dataset(gamewise).csv", index=False)
print("CSV file has been successfully created.")
