import pandas as pd

df = pd.read_csv('pandas_cleaning2.csv')

df.drop_duplicates(inplace = True)

print(df.to_string())
