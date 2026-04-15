import pandas as pd
from scipy.io import arff

data, meta = arff.loadarff("Rice_Cammeo_Osmancik.arff")
df = pd.DataFrame(data)

print(df.head())
print(df.columns)
print(df.dtypes)
