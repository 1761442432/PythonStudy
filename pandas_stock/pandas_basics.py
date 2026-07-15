import pandas as pd
import os
import openpyxl  # 读取文件需要的包

# Series：一维数组（带索引（可以理解为带标签的一列数据）），index定义索引，不定义则默认：0,1,2... 
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# DataFrame：二维表格，由多个 Series 组成，有行索引和列名。
df = pd.DataFrame(
    {
        'name':['张三', '李四', '王五'],
        'age':[10, 20, 30],
        'city':['厦门', '上海', '北京']
    }
)

# 获取当前脚本所在目录: ..\PythonStudy\pandas_stock
dirname = os.path.dirname(__file__)
# os.path.join 会自动处理路径分隔符跨平台兼容（Windows 用 \，Linux/Mac 用 /）
file_path = os.path.join(dirname, 'pandas学习.xlsx')
# 读取文件
df = pd.read_excel(file_path)
file_path_cvs = os.path.join(dirname, 'pandas学习.cvs')
df.to_csv(file_path_cvs, index=False)  # # 导出到 CSV：index=False 表示不保存行号

# 查看前 5 行
df.head()
# 查看后 5 行
df.tail()
# 整体信息：行数列数、各列类型、缺失值情况
# df.info()
# 对数值列做统计：计数、均值、标准差、四分位数等
# round(2) 保留2位小数
df.describe().round(2)


# 删除含 NaN 的行：不会改变excel文件
df_clean = df.dropna(inplace=False)  # 当inplace默认False， 当inplace=True 直接修改原数据 df 变量
# 填充 NaN，比如用 0 或均值填充
df_clean = df.fillna(0)  # 当inplace默认False， 当inplace=True 直接修改原数据 df 变量
# 使用job_id的平均值，填充 job_id 中为 Nan 的值
df_clean['job_id'] = df['job_id'].fillna( df['job_id'].mean() )  # df['job_id'] 不支持使用inplace=True，因为修改的是副本 
# 去除重复行
df_clean = df.drop_duplicates()
# 把某列转为数值（可能将'1,000'变成1000）
df_clean['job_id'] = pd.to_numeric( df['job_id'], errors='coerce' ) # errors='coerce' 无法解析的值变成 NaN，不报错
# 转为字符串
df_clean['job_id'] = df['job_id'].astype(str)

# 筛选 job_id>4 的行
result = df[ df['job_id']>4 ]
# 筛选 多条件：job_id>4 且 city是'成都'
result = df[ (df['job_id']>4) & (df['city']=='成都') ]
# 选中某几列
result = df[ ['job_name', 'city', 'salary'] ]
# 用 .loc 按行列标签选 ： 筛选 job_id>4 的行， 只展示这几列：'job_name', 'city', 'salary'
result = df.loc[ df['job_id']>3, ['job_name', 'city', 'salary']  ]

# 记住口诀：分组 → 选列 → 聚合
# 以 education 进行分组，计算每个组的 size 的平均值
result = df.groupby('education')['size'].mean()
# 以 education、salary 进行分组，计算每个组的 size 的最大值
result = df.groupby( ['education', 'salary'] )['size'].mean()
# 以 education 进行分组，计算每个组的 size 的平均值、最大值、行数
result = df.groupby( 'education' )['size'].agg( ['mean', 'max', 'min'] )
# 以 education 进行分组，计算每个组的 size 的平均值， job_id的最大值
result = df.groupby( 'education' ).agg(
    {
        'size':'mean',
        'job_id':'max'
    }
)

df2 = df
# 数据拼接   concat()：上下堆叠或左右拼合
# axis=0 ：竖直拼接（增加行）
df_join = pd.concat([df, df2], axis=0)
# axis=1 ：水平拼接（增加列）
df_join = pd.concat([df, df2], axis=1)
# 数据拼接   merge()：像 SQL 的 JOIN，按共同列匹配
# how 常用：inner（交集）、left、right、outer（并集）
# on='job_id'： 按 '用户ID' ,把 df、 df2 两个表关联起来
df_join = df.merge(df2, on='job_id', how="inner")

# print(df_join)
