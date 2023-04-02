
#线性查找：查找出某个字母在列表中的索引位置
def search(arr, x):
    for i in range(0, len(arr)):       #使用for循环，依次判断 x 是否在arr列表中存在
        if (arr[i] == x):
            return i
    return -1


if __name__ == '__main__':
    # 在数组 arr 中查找字符 D
    arr = ['A', 'B', 'C', 'D', 'E']
    x = '1'
    result = search(arr,  x)
    if (result == -1):
        print("元素不在数组中")
    else:
        print("元素在数组中的索引为", result)