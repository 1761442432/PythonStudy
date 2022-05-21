import pandas

"""
loc     用label（标签，比如key名）定位数据
iloc    用position（位置，比如第1行）定位数据
"""

# 打开的文件路径
path = 'D:\我的学习资料\编程学习\PythonStudy\pandas学习\学习成绩.xlsx'
df = pandas.read_excel(path)
print("查看文件的数据 （备注：pandas最左侧是索引）\n",df)

print("查看第3行的数据\n", df.iloc[3])
print("查看第2-5(iloc也是从0开始的，不包括5)行的数据\n", df.iloc[2 : 5])
print("查看第2-5(不包括5)行； 2-5列（不包括5）的数据\n", df.iloc[2 : 5, 2 : 5])

# 遍历第2行的数据
for x in df.iloc[2]:
    print("遍历第2行的数据", x)