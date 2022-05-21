import pandas

"""

"""

# 打开的文件路径
path = 'D:\我的学习资料\编程学习\PythonStudy\pandas学习\学习成绩.xlsx'
df = pandas.read_excel(path)
print("查看文件的数据 （备注：pandas最左侧是索引）\n",df)
# df.sort_values()：
#       axis：0按列排序（默认），1按行排序；       by 排序的标签名;
#       ascending：True为升序（默认）， False为降序;    inplace： True直接改变数据， False不改变数据，只返回数据（默认）
df.sort_values(axis=0, by='语文', ascending=False, inplace=True)
print("按语文成绩列（倒序）排序，inplace=True所以直接打印df生效了\n", df)
print("按语文成绩列（倒序）、数学成绩（升序）排序\n", df.sort_values(by=['语文', '数学'], ascending=[False, True]))
print("对第11行进行排序\n", df.sort_values( axis=1, by=11))
print("求语文成绩的平均分\n", df['语文'].mean())
print("去除pandans中的NaN空值\n",df )
# 备注： df.dropna() 是临时的，不会直接对df生效
print("去除pandans中的NaN空值（当某一行的其中一个字段存在空值，就会把整行去除）\n",df.dropna() )
print("去除pandans中的NaN空值\n",df )

print("英语列的第6到最后1行", range(len(df['英语']) )[6:])


