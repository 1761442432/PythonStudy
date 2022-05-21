import numpy as np
import statsmodels.api as sm
from matplotlib import pyplot as plt


# statsmodels 安装：pip install statsmodels
data_high = np.arange(2, 20, 2)
data_low = np.arange(1, 19, 2)
# 绘图并且显示图
# plt.plot(data_low, data_high)
# plt.show()

X = sm.add_constant(data_low)
model = sm.OLS(data_high, X)
results = model.fit()
a = []
a.append(results.params)
print(X)
print(a)
# 根据 R-Squared 的取值，来判断模型的好坏：
# 如果结果是 0，说明模型拟合效果很差；如果结果是 1，说明模型无错误。
# 一般来说，R-Squared 越大，表示模型拟合效果越好。
# R-Squared 反映的是大概有多准，因为，随着样本数量的增加，R-Square必然增加，无法真正定量说明准确程度，只能大概定量。
print(results.rsquared)