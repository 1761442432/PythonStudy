
list_num = [0, 22, 1, 6, 24, 99, 21, 87]

# 对列表、元组等进行切片。[a:b]从索引a开始（包括），到索引b结束（不包括）
# 字典不能进行切片，因为字典是无序的，没有索引
print(list_num[1:6])

# 计算容器（列表、字典、字符串等）中元素的个数
print(len(list_num))

# 删除变量
del(list_num[2])

# 返回容器中最大的元素
print(max(list_num))

# 返回容器中最小的元素
print(min(list_num))

# 将容器（列表、字典、字符串）中所有元素 * 3
print(list_num * 3)

# 将容器（列表、字典、字符串）后面追加列表
print(list_num + [1, 2, 3])

# 判断容器（列表、字典、字符串、字典）中是否包含某个元素。包含返回True， 否则返回False
# 备注：字典 判断的是key是否包含
print("a" in {"a":"bcc"})

# 判断容器（列表、字典、字符串、字典）中是否包含某个元素。不包含返回True， 否则返回False
print("a" not in "lllssxv")