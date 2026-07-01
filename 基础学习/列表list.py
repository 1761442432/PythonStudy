
# 定义一个字符串变量：name
name = "zhangshan"

# 定义一个list变量:name_list. python 支撑存储不同的数据类型
name_list = []
name_list = ["zhangsan", "lisi", "wangwu", 1]

# 打印列表，    打印列表第0个元素:zhangsan
print(name_list, name_list[0])

# name_list.index("zhangsan") 打印zhangsan所在的索引位置。如果zhangsan不存在，则程序报错
print(name_list.index("zhangsan"))

# 修改“索引1”为“李四”，如果索引超出范围，则程序报错
name_list[1]  = "李四"

# 往列表最后的位置，追加数据
name_list.append("王小二")

# 往列表"索引1"的位置，插入数据
name_list.insert(1, "王大")

# 往列表最后的位置，追加另一个列表所有的数据
temp_list = ["临时_小王", "临时_小王", "临时_小王"]
name_list.extend(temp_list)

# remove 方法可以从列表中删除指定数据
name_list.remove("zhangsan")

# pop 方法默认删除最后一个位置的数据；如果传入索引后，删除索引所在位置的数据
name_list.pop(2)

# del 从内存中删除变量。在日常开发中，建议使用列表提供的方法删除数据（不要使用del）
del name_list[1]
# del 删除变量后，name将不可使用
del name
# print(name)
# 清空列表。将所有数据删除
# name_list.clear()

# 计算列表的长度
len(name_list)

# 计算列表中某个数据出现的次数
name_list.count("临时_小王")
# 打印列表
print(name_list)

num_list = [2,4,1,3,10,8]
#  （默认reverse=False）升序排序，  reverse=True 降序排序
# PS：中文、英文 默认首字母排序
num_list.sort()
num_list.sort(reverse=True)

# 逆序排序（从后往前排序）
num_list.reverse()

# 列表遍历
for num in num_list:
    print(num)

print("打印列表：",num_list)

list_for = [6,2,9,3]
# min() 返回最小的数据
print("min(test)=   ",min(list_for))

# 将list_for的值赋值给i，然后生成一个二维数组
# 结果：list_for = [[1, 123, 234, 456], [2, 123, 234, 456], [3, 123, 234, 456]]
list_for_result = [[i, 23, 1, 20] for i in list_for]
print("list_for_result=   ",list_for_result)

# list.sort( key=None, reverse=False) ：没有返回值，对列表进行返回。默认升序，reverse=True时，降序；
# key 是排序的元素。如：key=lambda a:a[1] 是按数组的索引=1的元素为进行排序（a 可以替换为任意字母）(好像这种只适合二维数组，一维数组不适合)
list_sortTest = [[23, 2, 4, 1], [28, 4,1, 9], [22, 3, 5, 0]]
list_sortTest.sort(key=lambda a:a[1], reverse=True)
print("list_for_result.sort()=  ",list_sortTest)

totalcount = [[1,2,3], [2,2,1], [2,34,5]]
rank_stock_list = [2222, 1111, 5555]
qq = [rank_stock_list[totalcount[2-i][0]] for i in range(2)]
print(qq)
print(totalcount[-1 - 1] [0])
for i in range(0):
    print("2222222",i)

print("--------------------------")
list = [1,2,35,1,2,43]
1 in list
print(1111 in list)
print("计算列表的和：", sum(list))