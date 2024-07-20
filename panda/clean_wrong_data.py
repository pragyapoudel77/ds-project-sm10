import pandas as pd

df = pd.read_csv('pandas_cleaning2.csv')

df.loc[7,'Duration'] = 45

print(df.to_string())