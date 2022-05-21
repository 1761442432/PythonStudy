import statsmodels.api as sm
import pandas as pd

"""
path1 = 'D:/我的学习资料/编程学习/PythonStudy/numpy/test1_high.xlsx'
path2 = 'D:/我的学习资料/编程学习/PythonStudy/numpy/test2_low.xlsx'

df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)


df1.set_index(list(df1)[0], inplace = True)
df2.set_index(list(df2)[0], inplace = True)

data_high = df1.iloc[ : , 0]
data_low = df1.iloc[ : , 0]

print(df1 )

"""


data_high = pd.Series([2.23, 2.23, 2.26, 2.28, 2.27, 2.20, 2.19, 2.14, 2.06, 2.08, 2.05, 2.10, 2.15, 2.15, 2.13, 2.08, 2.04, 1.98])
data_low = pd.Series([2.17, 2.17, 2.18, 2.24, 2.17, 2.15, 2.15, 2.01, 2.01, 2.03, 1.94, 1.99, 2.06, 2.07, 2.06, 2.03, 1.97, 1.89])
print(data_high)
print(data_low)

# 进行线下回归
X = sm.add_constant(data_low)
model = sm.OLS(data_high, X)
results = model.fit()
print(results.summary())
print(results.params)
print("----------------", results.params[0])