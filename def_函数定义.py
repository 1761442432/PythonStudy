
# 不能放在 函数定义的上方，因为 python 是 从上往下 执行代码的
# printTest()

# python 和 java 一样，定义一个函数后需要 调用 才会执行
def printTest(num1, num2):
    """ 这个是函数说明：调用函数时，可按快捷键 ctrl + Q 查看函数说明 """
    print("hallo test1")
    print("hallo test2")
    # return 是函数结束，之后的代码不会执行
    return num1+num2

#  调用函数，调用后就会执行
sum_num = printTest(10, 20)
print("计算结果为：%d"  % (sum_num))


def printString(char, time):
    """
    自定义字符，并自定义字符重复的次数，然后打印字符串
    :param char:    需要打印的字符
    :param time:    字符重复的次数
    :return:
    """
    print("打印字符串：",char * time)

def printStrings(char, time):
    """
    循环5次，打印字符串
    :param char: 需要打印的字符
    :param time: 字符重复的次数
    :return:
    """
    num = 0
    while num < 5:
        printString(char, time)
        num += 1

printStrings("*", 20)