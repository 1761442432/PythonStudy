import numpy as np
from matplotlib import pyplot as plt

# numpy 安装：pip install numpy
# matplotlib安装：pip install matplotlib

# 使用 numpy生成数组（一维）：
t1 = np.array([1,2,3])
print("打印numpy的数据：", t1)
print("numpy.ndarray类型：",type(t1))
# 结果： (3,) 表示 3个元素（长度），说明是一个一维数组
print("查看数组的形状：", t1.shape)

print("range(10) 返回 0-9的数字：", np.array( range(10) ) )
print("arange()是numpy自带的方法，也是返回0 -9 的数字：", np.arange(10))
print("arange(3, 6)是返回3 -5 的数字：", np.arange(3, 6))
print("arange(3, 10, 2)是：3开始，10结束。返回：3、3+2、3+2+2、3+2+2+2：", np.arange(3, 10, 2))

# 使用 numpy生成数组（二维）：每个一维数组的长度要一样
t2 = np.array([ [1, 2, 3, 4], [2, 3, 4, 5], [1, 4, 5, 8] ])
print("打印numpy的数据\n", t2)
# (3, 4) ：2个数字表示2维数组， 3表示里面有3个数组，4表示每个数组长度是4
print("查看数组的形状：", t2.shape)

# 使用 numpy生成数组（三维）：每个一维数组、二维数组的长度要一样
t3 = np.array([ [[1,2,3,4],[2,3,4,5]]  , [[11,12,14,15],[13, 11, 2,5]], [[1,2,3,1],[2, 2,2,2]] ])
print("打印numpy的数据\n", t3)
#  (3, 2, 4) ：3个数字表示3维数组。3表示有3个2维数组，2表示每个二维数组的有1个一维数组， 4表示每个一维数组的长度是4。
print("查看数组的形状：", t3.shape)