import pandas as pd
import os
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# 读取文件
path = os.path.dirname(__file__)
path_file = os.path.join(path, "data.csv")
# index_col=0 第0列为索引； parse_dates=True 自动尝试解析所有看起来像日期的列为 datetime 类型
df = pd.read_csv(path_file, index_col=0, parse_dates=True)

#  kind='bar' 条形图展示;  line：折线图（默认值）；  area：面积图  scatter：散点图
#  title：设置图表标题（字符串）
#  xlabel / ylabel：设置 X 轴和 Y 轴的标签名
#  color：设置颜色（如 'red'、'#FF0000'，或传入与列数相同的颜色列表）
#  style：设置线条和标记样式（如 'o-' 表示带圆点的实线，'--' 表示虚线, '-'默认实线）
#  subplots： True 多个子图， False 一个图
df.plot(kind='line', title='Test', xlabel='Date', color='red', style='--', figsize=(10, 6), subplots=False)

# 第二个图：subplots： True 多个子图， False 一个图
df[ ['AAPL.O', 'MSFT.O','INTC.O'] ].plot(kind='line', title='Test 2', color='blue', subplots=True)

# 第三个图：secondary_y='.VIX'    .VIX这一列绘制在图表的右侧次坐标轴（Secondary_y） 上
# 日期范围：开头 -- 2011/4/7
df[ ['AAPL.O', '.VIX'] ].loc[:'2011/4/7'].plot(kind='line', title='Test 3', subplots=False, secondary_y='.VIX')

'''
绘制散点图矩阵：
pd.plotting.scatter_matrix ：会生成一个 N*N 的网格图(N 是 rets 的列数）
alpha=0.2 设置散点的透明度为 20%(0 为完全透明,1 为完全不透明），颜色越深的地方，代表数据点越密集
diagonal='hist'直方图  kde(曲线图）， 观察单只资产收益率的分布形态。你可以直观地检查它是否接近正态分布（钟形曲线），或者是否存在明显的“左偏/右偏”
hist_kwds={'bins':50}  表示将数据范围切分成 50 个区间（柱子），观察收益率分布的 “肥尾”现象（即极端大涨或大跌的发生频率是否高于正态分布的预测）
figsize=(10,6) 设置整个大图表的物理尺寸为 10 英寸宽,6 英寸高

图形说明：
左上角:AAPL 自己的"成绩分布"
    -- 中间的柱子最高 → 说明大多数日子涨跌幅接近 0(不涨不跌)
    -- 两边矮 → 说明大涨或大跌的日子很少
右下角:VIX 自己的"成绩分布"
    -- 柱子集中在左边 → 说明大多数日子 VIX 是下跌的（市场平静）
    -- 右边有长长的尾巴 → 说明偶尔会暴涨（市场恐慌）
右上角 & 左下角:AAPL 和 VIX 的"关系图"((左下角:AAPL 在 X 轴,VIX 在 Y 轴））
    -- X 轴:AAPL 的涨跌幅（往右是涨，往左是跌）
    -- Y 轴:VIX 的涨跌幅（往上是涨，往下是跌）
'''
data = df[ ['AAPL.O', '.VIX'] ]
rets = np.log(data/data.shift(1))
pd.plotting.scatter_matrix(
    rets,
    alpha=0.2,
    diagonal='hist',
    hist_kwds={'bins':50},
    figsize=(10,6)
)

plt.show()     # 显示所有图形