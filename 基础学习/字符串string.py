
str1 = "hello hello"       # 定义一个字符串
str2 = '你好啊，"大西瓜"'    # python中，'' 号也可以定义字符串，并且里面可以使用""号
print(str1[2])  # 字符串也可以通过索引进行获取字符。遍历的方式同列表list
print(str2)

# 统计字符串的长度
print(len(str1))

# 统计 子字符串 出现的次数
print(str1.count("llo"))

# 某一个字符串出现的位置.如果不存在，则报错
print(str1.index("llo"))

# 判断字符串是否是空白字符。是返回True，否则返回false。注意：\n\t\r也是空白字符
print("  \n\t\r".isspace())

# 判断字符串是否是纯数字，是 返回True，否则 false
print("1".isdecimal())

# 判断字符串是否是纯数字、全角数字，是 返回True，否则 false
print("①".isdigit())

# 判断字符串是否是纯数字、全角数字、中文数字，是 返回True，否则 false
print("一千零一".isnumeric())

# 判断字符串是否以知道 子字符串 开始。是 返回True，否则 false
print("hello world".startswith("hello"))

# 判断字符串是否以知道 子字符串 结束。是 返回True，否则 false
print("hello world".endswith("world"))

# 查找指定字符串的索引位置。如果不存在，返回 -1
print("hello world".find("llo"))

# 替换字符串(需要替换的字符串 ,  替换后的字符串)，然后返回一个新的字符串
print("hello world".replace("world", "python"))

# 以子字符串的位置分隔，返回一个list列表。默认以 空格 分隔
print("白日 哈哈哈".split("日"))