import csv

movie_data = []
with open('data\movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movie_data.append(row)

ratings_data = []
with open('data\\ratings.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ratings_data.append(row)

tags_data = []
with open('data\\tags.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tags_data.append(row)

movie_tags = {}
for tag in tags_data:
    movie_id = tag['movieId']
    if movie_id not in movie_tags:
        movie_tags[movie_id] = [tag['tag']]
    else:
        movie_tags[movie_id].append(tag['tag'])

for movie in movie_data:
    movie_id = movie['movieId']
    if movie_id in movie_tags:
        movie['tags'] = '|'.join(movie_tags[movie_id])
    else:
        movie['tags'] = None

movie_ratings = {}
for rating in ratings_data:
    movie_id = rating['movieId']
    if movie_id not in movie_ratings:
        movie_ratings[movie_id] = [float(rating['rating'])]
    else:
        movie_ratings[movie_id].append(float(rating['rating']))

average_ratings = {}
for movie_id, ratings in movie_ratings.items():
    average_ratings[movie_id] = sum(ratings) / len(ratings)

for movie in movie_data:
    movie_id = movie['movieId']
    if movie_id in average_ratings:
        movie['average_rating'] = average_ratings[movie_id]
    else:
        movie['average_rating'] = None

fieldnames = ['movieId', 'title', 'genres', 'tags', 'average_rating']
with open('../movie_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movie_data:
        writer.writerow(movie)

print("CSV file has been successfully created.")
