import pandas as pd
import os
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# 读取文件
path = os.path.dirname(__file__)
path_file = os.path.join(path, "stock_data_2026_6.xlsx")

# -------------------- 图标显示， 多个指标汇总 -----------------
# index_col=0 第0列为索引； parse_dates=True 自动尝试解析所有看起来像日期的列为 datetime 类型
df = pd.read_excel(path_file, index_col=0, parse_dates=True) 
# figsize=(5,11) 控制窗口大小； subplots=True 拆分为多个子图（默认False）
# df.plot(figsize=(10, 12), subplots=True) 
# plt.show()  # 显示图窗，不加这行在脚本运行时不会弹出窗口
# 多个指标汇总
data = df.aggregate( [min, max, np.mean, np.std, np.median] )


# ------------------- 序列变化情况计算 ---------------- 
# 计算每一天的差异值（后一天减去前一天结果）
data = df.diff()
# 计算每一天的差异率（ (后一天减去前一天结果) / 前一天值 )
data = df.pct_change().round(4)
# kind='bar' 条形图展示
data.mean().plot(kind='bar', figsize=(10, 6))

print(data)