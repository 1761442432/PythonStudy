
# 字典是一个无序的数据集合。使用print打印字典时，顺序是无序的
xiaoming_dict = {"name":"小明", "age":18, "gneder":True, "height":1.75}    #定义一个字典

# 打印key对应的value。如果key不存在，会报错
print(xiaoming_dict["name"])

# 如果key存在，则修改key对应的value值修
# 如果key不存在，则新增一堆“键值对（key value）”
xiaoming_dict["age"] = 19

# 删除指定的key。（如果key不存在，则报错）
xiaoming_dict.pop("name")

# 字典的长度。（键值对的数量）
print(len(xiaoming_dict))

temp_dict = {"temp":"dict", "age":22}
# 合并字典。如果合并的字典中，key存在，则更新key对应的数据
xiaoming_dict.update(temp_dict)

# 清空字典
# xiaoming_dict.clear()

# 遍历字典。 注意：key_temp 是获取到的key
for key_temp in xiaoming_dict:
    print(key_temp, "--", xiaoming_dict[key_temp])

print(xiaoming_dict)
