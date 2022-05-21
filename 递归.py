
"""
递归函数的特点：
    1、自己调用自己
    2、必须要有一个函数的出口，否则会出现死循环
    3、递归（自己调用自己）前面的代码为正循环（相当于for循环）
        递归（自己调用自己）之后的代码，要等前面的代码循环结束后执行，然后逆循环
"""
def printNum(num):
    print("printNum-num", num)
    # if 是函数的出口，当num==1时，方法结束
    if num == 1:
        return
    # 函数自己调用自己
    printNum(num-1)
    print("printNum-哈哈哈哈",num)

printNum(3)
"""
结果：
num 3
num 2
num 1
哈哈哈哈 2
哈哈哈哈 3
"""

# 计算 1+2+3...num的和
def sum_numbers(num):
    if num == 1:
        return 1
    temp = sum_numbers(num-1)
    return temp+num

print(sum_numbers(100))
