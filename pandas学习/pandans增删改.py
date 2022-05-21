import pandas as pd

# 创建DataFrame
data = {
    'state':['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
    'year':[200, 201, 202, 203, 204],
    'pop':[1.5, 1.6, 1.7, 1.8, 2.0]
}
df = pd.DataFrame(data)
print(df)
