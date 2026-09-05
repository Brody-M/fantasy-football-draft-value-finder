import pandas as pd

df = pd.read_csv("NFLData_cleaned.csv")

print(df.head())
print(df.shape)
print(df.columns.tolist())