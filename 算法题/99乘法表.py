
def sum99():
    """
    打印 99 乘法表
    :return:
    """
    for i in range(1, 10):
        for j in range(1, i+1):
            print('{}*{}={}'.format(i, j, i * j))
        print()

if __name__ == '__main__':
    sum99()