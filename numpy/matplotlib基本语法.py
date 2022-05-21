import numpy as np
from matplotlib import pyplot as plt

# numpy 安装：pip install numpy
# matplotlib安装：pip install matplotlib

x = [1,2,3,4,6]
y = [2, 4, 6, 8, 10]

# 设置图形大小：figsize=(长,宽)， dpi 像素（越大越清晰）
# plt.figure(figsize=(20, 8), dpi=80)
# 绘图 plot(x, y) 分布表示 x轴、Y轴
plt.plot(x, y)
# 保存图片，一般保存都是先绘图，然后保存
# plt.savefig('./matplotlib第一张图.png')
# 显示图形
plt.show()
