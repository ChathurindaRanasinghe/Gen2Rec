import json

import pandas as pd

json_file = 'data/laptop_scraped.json'


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + ' ')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + ' ')
                i += 1
        else:
            out[name.strip()] = x

    flatten(y)
    return out


with open(json_file, 'r') as file:
    data = json.load(file)

flattened_data = []

for item in data:
    flattened_item = flatten_json(item)
    flattened_data.append(flattened_item)

df = pd.DataFrame(flattened_data)

columns_to_check = ['Additional Information Date First Available',
                    'CPU CPU Name',
                    'CPU CPU Type',
                    'Dimensions & Weight Dimensions (W x D x H)',
                    'Dimensions & Weight Weight',
                    'Display Screen Size',
                    'Memory Memory',
                    'Model Brand',
                    'Model Model',
                    'Storage HDD',
                    'Storage SSD']

df_filtered = df.dropna(subset=columns_to_check, how='any')

df_filtered.to_csv('../laptop_dataset.csv', index=False)

print("CSV file has been successfully created.")
