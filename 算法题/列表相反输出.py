
def myReverse(arr):
    """
    对列表进行相反输出：将列表使用for循环，从最后一个元素开始 到 第0个元素，依次添加新的列表
    :param arr:
    :return:
    """
    arr2 = []
    arrLen = len(arr)
    for i in range(len(arr)-1, -1, -1):
        arr2.append(arr[i])
    return arr2
if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6]
    arr.reverse()
    print("使用reverse对列表相反输出：",arr)
    print("使用自创函数对列表相反输出：",myReverse(arr))
