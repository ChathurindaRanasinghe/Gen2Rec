import pandas as pd
import json
from dataset_utils import json_to_dataframe
from pprint import pprint


pd.set_option('display.max_columns', None)

with open("datasets/laptop-dataset/data/raw_data_mp3_15_Feb_2024_22_25_14.969302.json", "r") as f:
    laptop_data = json.load(f)
    laptop_df = json_to_dataframe(laptop_data)


pprint(laptop_df.shape)

# Remove laptops that do not have either a brand or model
laptop_df.columns = laptop_df.columns.str.strip()
# print(laptop_df.columns)
laptop_df.dropna(subset=['Model.Brand', 'Model.Model'],how='any',inplace=True)
laptop_df.drop(columns=laptop_df.columns[0], axis=1, inplace=True)
laptop_df.reset_index(drop=True)
laptop_df.drop(columns=laptop_df.columns[0], axis=1, inplace=True)

cols = []

for col in laptop_df.columns:
    if "Quick Info." in col:
        continue
    cols.append(col)

laptop_df = laptop_df[cols]

laptop_df.to_csv('laptop.csv')
