
# ps：元组与列表类似， 但是元组不能修改数据
empty_tuple = ()     # # 定义一个空元组。 实际开发中很少定义空元组，因为元组不能修改数据
one_tuple = (5,)     # 定义只有一个数据的元祖时需要加上","  否则他的类型是int型
info_tuple = ("张三", 19, 1.99, "张三")  #元组也可以存储不同的数据类型

# 获取元组索引位置的数据
print(info_tuple[1])

# 获取元组数据所对应的索引
print(info_tuple.index("张三"))

# 统计元祖中数据重复出现的次数
print(info_tuple.count("张三"))

# 循环遍历元组
for info in info_tuple:
    print("正在循环遍历元祖：", info)

num_list = [1,23, 2]

# 返回： list（列表） 转换为 tuple（元组）
tuple(num_list)

# 返回：tuple（元组） 转换为 list（列表）
list(info_tuple)

