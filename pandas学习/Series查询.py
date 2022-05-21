import pandas

# 打开的文件路径
path = 'D:\我的学习资料\编程学习\PythonStudy\pandas学习\学习成绩.xlsx'
df = pandas.read_excel(path)

print("打印所有数据\n",df)
print("获取所有语文成绩（得到的是Series）\n", df['语文'])
print("获取所有语文成绩（得到的是Series）\n", type(df['语文']) )

print("获取所有语文成绩的平均分\n", df['语文'].mean())
print("获取所有语文成绩最大分数\n", df['语文'].max())
print("获取所有语文成绩最小分数\n", df['语文'].min())
print("获取所有语文成绩第一个分数（head不加1的话，会返回4行不知道为啥）\n", df['语文'].head(1))   # 不能用于if判断
print("获取所有语文成绩最后2个分数\n", df['语文'].tail(2))
print("获取所有语文成绩第一个分数\n", df['语文'].iloc[-1]) # 可以用于if判断



