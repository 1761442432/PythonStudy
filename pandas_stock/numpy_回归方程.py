
import pandas as pd
import os
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# 读取文件
path = os.path.dirname(__file__)
path_file = os.path.join(path, "data.csv")
df = pd.read_csv(path_file, index_col=0, parse_dates=True)

'''
构建回归方程：对 ['.SPX']、['.VIX']进行线性回归，可视化 SPX 和 VIX 之间的负相关关系
使用最小二乘法, 对标准普尔500指数(.SPX)和恐慌指数(.VIX)之间的关系进行“一元线性回归”拟合。
np.polyfit(x, y, deg=1):x、y 必须是一维数组或 Pandas Series。
  -- x自变量, y因变量, deg=1 线性拟合（一次多项式）； deg=2 二次曲线拟合（抛物线）； deg=3 是三次曲线，以此类推
  -- 对于 deg=1,它会返回一个包含两个元素的数组：[斜率 (m), 截距 (c)]
'''
# 剔除 NaN 值，否则 np.polyfit 会报错
data = df[ ['.SPX', '.VIX'] ]
rets = np.log(data/data.shift(1))
rets.dropna(inplace=True)
# 公式y=ax+b，构建回归，根据x、 y算出：[a, b]：   
result = np.polyfit(rets['.SPX'], rets['.VIX'], deg=1)

# 图形展示：从图形中，可以看出 他们直接负相关，既：恐慌指数上涨时，SPX下跌
#    -- X 轴:.SPX 的涨跌幅（往右是涨，往左是跌）
#    -- Y 轴:VIX 的涨跌幅（往上是涨，往下是跌）
ax = rets.plot(kind="scatter", x='.SPX', y=".VIX", figsize=(10,6))

'''
趋势线：查看 SPX 和 VIX 的负相关关系趋势
公式y=ax+b , np.polyval([a,b], x) : 算出y的值
为何要用 np.polyval:
  -- rets['.VIX'] 是真实值（包含噪音，得到一条锯齿状、弯弯曲曲的折线） 
  -- np.polyval(...) 是预测值/理论值（得到的是：直线）
'''
ax.plot(rets['.SPX'], np.polyval(result, rets['.SPX'] ), color='red' )
plt.show()  # 为了不影响下面的展示，需要先把上面的显示出去


'''
皮尔逊相关系数：用 -1 到 1 之间的数字，来精确量化两个变量之间的线性相关程度
  -- 输出：
               .SPX      .VIX
        .SPX  1.000000 -0.806532
        .VIX -0.806532  1.000000
  -- 对角线上的值:1.000000(没多大意义） : 任何变量与自身的相关性永远是完美的 1.0(100% 正相关)
  -- 非对角线上的值：-0.806532 : 符号是负的(-) 代表负相关，绝对值越大，代表相关性越强
'''
print ( rets.corr() )

# 250日K线，展示  ['.SPX']、['.VIX'] 的皮尔逊相关系数
rets['.SPX'].rolling(window=250).corr( rets['.VIX']).plot(figsize=(10, 6))
plt.show()


