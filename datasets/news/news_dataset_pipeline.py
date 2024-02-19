import pandas as pd

df = pd.read_csv("world news in month.csv", encoding = 'latin1')

df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'] >= '2018-11-01') & (df['Date'] <= '2018-11-10')]
# df = df[df['name'] == 'UK']
print(df.shape)

df.drop(columns=['sentiment'], inplace=True)

df.drop(columns=df.columns[0], axis=1, inplace=True)
print(df.columns)
df.to_csv("news.csv", index=False)

