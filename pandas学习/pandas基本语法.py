import pandas

# pandas 安装：pip install pandas
# 如果安装之后无法导入包，可以选择右上角的 "向下箭头" 安装pandas
# 如果无法打开文件，提示“No module named 'openpyxl'”
    # 可以安装下openpyxl包：pip install openpyxl

"""
pandas基本知识：
1、pandas的数据类型分为 dataFrame（二维数据；多行多列） 和 Series（一位数据；单行单列）
2、从DateFrame中查询Series
    如果查询一行、一列，返回的是pandas.Series
    如果查询多行、多列 返回的是pandas.DataFrame
"""
# 打开的文件路径
path = 'D:\我的学习资料\编程学习\PythonStudy\pandas学习\学习成绩.xlsx'
# 读取文件（xlsx文件使用read_excel() 方法）
# cvs/txt 文件使用 read_cvs(); mysql数据表使用 read_sql()
df = pandas.read_excel(path)

# 将“日期”列设置为索引。inplace = True时，永久改变当前对象； 否则只是暂时改变
df.set_index('日期', inplace = False)
# 将第一列设置为索引
df.set_index(list(df)[0], inplace = False)
print("查看文件的数据 （备注：pandas最左侧是索引）\n",df.head())
print("查看索引（行）\n",df.index)
print("查看索引（列）\n",df.columns)
print("查看每列的数据类型\n",df.dtypes)

# 创建Series
s1 = pandas.Series(['b', 'a', 5, 2, 7])

print("Series类型\n", s1)
print("Series获取索引\n", s1.index)
print("Series获取数据\n",s1.values)
print("获取索引位置的数据\n",s1[1])
print("获取索引位置的数据类型\n",type(s1[1]))
print("获取Series的多个索引数据\n",s1[[1, 3]] )

# 创建DataFrame
data = {
    'state':['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
    'year':[200, 201, 202, 203, 204],
    'pop':[1.5, 1.6, 1.7, 1.8, 2.0]
}
df = pandas.DataFrame(data)
print("打印DataFrame数据\n",df)
print("DataFrame的类型\n", df.dtypes)
print("DataFrame的索引（列）\n", df.columns)
print("DataFrame的索引（行）\n", df.index)

# 从DateFrame中查询数据
print("查询单列数据\n", df['year'])
print("查询单列数据返回的是Series类型\n", type(df['year']))
print("查询多列数据\n",df[['year', 'pop']])
print("查询多列返回的是DataFrame类型\n", type(df[['year', 'pop']]))
print("查询单行数据（1是索引）\n", df.loc[1])
print("查询单行数据（1是索引）返回的是Series类型\n",type(df.loc[1]) )
print("查询多行数据\n",df.loc[1:3])
print("查询多行数据返回的是DataFrame类型\n",type(df.loc[1:3]) )
print("查询部分字段的部分行（1、2行； 3行不包括）\n", df[['year', 'pop']][1 : 3])
