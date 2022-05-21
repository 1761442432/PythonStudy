import pandas

"""
loc     用label（标签，比如key名）定位数据
iloc    用position（位置，比如第1行）定位数据
"""

# 打开的文件路径
path = 'D:\我的学习资料\编程学习\PythonStudy\pandas学习\学习成绩.xlsx'
df = pandas.read_excel(path)
# 设定索引：以学号为索引
df.set_index('学号', inplace=True)
print("查看文件的数据 （备注：pandas最左侧是索引）\n",df.head())

print("获取第2行的日期字段（得到单个值）\n", df.loc[2, '日期'])
print("获取第2行的语文、数学字段（得到的是Series）\n", df.loc[2, ['语文', '数学'] ])
print("获取第2、3行的姓名字段（得到的是Series）\n", df.loc[[2, 3], '姓名'])
print("获取第2、3行的姓名、语文、数学字段（得到的是DataFrame）\n", df.loc[[2, 3], ['姓名','语文','数学'] ])
print("查询语文成绩在80分以上的数据（返回的是boolean类型）\n", df['语文']>80)
# df.loc[ df['语文']>80 , :] 与 df.loc[ df['语文']>80 ] 是一样的结果，都是返回所有列
print("查询语文成绩在80分以上的数据（返回的满足条件的所有列的数据）\n", df.loc[ df['语文']>=80 , :])
print("查询语文成绩在80分以上的数据（返回的满足条件的数据，只需要‘语文’字段）\n", df.loc[ df['语文']>=80 , ['语文']])
print("查询语文、数学、英语成绩都在80分以上的数据（语法规定：每个条件需要用括号括起来）\n", df.loc[ (df['语文']>=80) & (df['数学']>=80) & (df['英语']>=80) , :])
# lambda 的用法待确认
print("调用函数查询\n", df.loc[ lambda df : (df['语文']<80) ])
def getChineseAndMath(df):
    return (df['语文']>=80) & (df['数学']>=90)
print("编写自己的函数，查询数据\n", df.loc[ getChineseAndMath(df) ])

print("姓名=刘备的语文成绩平均分：\n", df.loc[ df["姓名"]=="刘备" , '语文'].mean() )
print("姓名=刘备的人有多少人\n", (df['姓名']=='刘备').sum() )
print("求语文的最大成绩\n", df.loc[ :, ['语文'] ].max())
print("求语文的最小成绩\n", df.loc[ :, ['语文'] ].min())

a = {}
b = [1,2,3]
a['aaa'] = b
a['aaa'].append(2222)
print(a)