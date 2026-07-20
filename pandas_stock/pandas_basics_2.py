import pandas as pd
import os
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# 读取文件
path = os.path.dirname(__file__)
path_file = os.path.join(path, "data.csv")

# -------------------- 图标显示, 多个指标汇总 -----------------
# index_col=0 第0列为索引； parse_dates=True 自动尝试解析所有看起来像日期的列为 datetime 类型
df = pd.read_csv(path_file, index_col=0, parse_dates=True)
# figsize=(5,11) 控制窗口大小； subplots=True 拆分为多个子图(默认False)
# df.plot(figsize=(10, 12), subplots=True) 
# plt.show()  # 显示图窗,不加这行在脚本运行时不会弹出窗口
# 多个指标汇总
data = df.aggregate( [min, max, np.mean, np.std, np.median] )


# ------------------- 序列变化情况计算 ---------------- 
# 计算每一天的差异值(后一天减去前一天结果)
data = df.diff()
# 计算每一天的差异率( (后一天减去前一天结果) / 前一天值 )
data = df.pct_change().round(4)
# 'line':折线图(默认值)； kind='bar' 条形图展示;  'area':面积图
# data.mean().plot(kind='bar', figsize=(10, 6))
data = data.mean()

# df.shift(1) 整体数据 往下 移动1行(第1行默认Nan)
# df.shift(-2) 整体数据 往上 移动2行(最后2行默认Nan)
data = df.shift(-1).head()
'''
df/df.shift(1):今天的值除以昨天的值 
    相对价格(1 + 简单收益率): 结果 > 1,说明资产增值了； 结果 < 1,说明资产贬值了
np.log(df/df.shift(1))
    np.log() :以 e 为底的对数
    主要用于时间上的“可加性” :假设本金 100 元。第一天涨 50%(变成 150),第二天跌 50%(变成 75)
    简单收益率不能直接相加:50%+(-50%)=0%,但实际上你亏了 25%!
    对数收益率可以直接相加:第一天ln(150/100)≈0.405, 第二天ln(75/150)≈-0.693,
                       总对数收益率0.405+(-0.693)=-0.288(可以通过公式转换为 -25%)
'''
data = np.log(df/df.shift(1))
# np.cumsum( [1, 2, 3, 4] :输出 [ 1  3  6 10]
# np.exp(x) :e的x次方, 既 np.log() 的逆运算(求相对价格)
data = data.cumsum().apply(np.exp)



# ------------------- 时间序列重采样 ---------------- 
'''
# '1w':代表重采样的时间窗口大小, 1m代表1月
# label='left' (默认 right)
#       窗口是 10月2日(周一) 到 10月6日(周五)
#       label='left'(左边界):其时间索引会被标记为窗口的起始时间,即 2023-10-02
#       label='right'(右边界):其时间索引会被标记为窗口的结束时间,即 2023-10-08
# last():提取时间最后的那一行,既 每周最后一个交易日的价格(pandas会自动获取,而不是固定周日)
'''
data = df.resample('1w', label='right').last()


'''
# rolling(window, min_periods=window):
#   - window=20(最大取值):每次取最近 20 个交易日
#   - min_periods=window(最小取值,不足时为Nan):前 window-1 天数据不足,输出 NaN
# 举例:     
#   - prices = pd.Series([10, 11, 12, 11.5, 13])
#   - print(prices.rolling(window=3, min_periods=2).mean())
#   - 输出:NaN(不足2天) 10.5(前两天平均值) 11.0(前3天的平均值) 11.5(11、12、11.5的平均值) 12.67(12、 11.5、 13的平均值)
# 说明:
#   - apply传参(一个数一个数传): 10   11    12   ... 
#   - rolling(3, 2).apply传参(一组一组传): 10   10,11   10,11,12  11,12,11.5  ... 
'''
data['m10'] = data['AAPL.O'].rolling(window=10).mean() # 10日均线
data['m90'] = data['AAPL.O'].rolling(window=90).mean() # 90日均线
# np.where(condition, x, y) :condition成立返回x, 否则返回y
data['positions'] = np.where( (data['m10']>data['m90']), 1, -1 )
# 指定将 positions 这一列绘制在图表的右侧次坐标轴(Secondary_y) 上
data[ ['AAPL.O', 'm10', 'm90', 'positions'] ].plot(figsize=(10, 6), secondary_y='positions')

# 展示图形
plt.show()
# print(np.exp(1))
print(data.head(30))