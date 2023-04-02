
#  冒泡排序：从小到大排序
# 说明：列表第一个 和 列表第二个 做比较，更大的话就互相交换位置；
# 然后 列表第二个 和 列表第三个 做比较，更大的话也是互相交换位置，
# 一直到最后2个数比较完成，这样就可以求出从小到大的顺序。
def bubbleSort(arr):
    for i in range(len(arr) - 1):                       # 只需要经过len(L)-1轮，排序即结束，i代表每一轮比较
        for j in range(len(arr)-1 ):                    # 这里面的i就是当前所在的轮数，j表示每一轮要遍历的元素
            if arr[j] > arr[j + 1] :                    # 假设当j=1时，这里是第一个元素和第二个比较
                arr[j],arr[j + 1] = arr[j + 1],arr[j]   # Python常用的交换变量写法
    return arr

if __name__ == '__main__':
    arr = [1, 9, 12, 3, 2, 5, 4, 9, 7]
    # arr[0] = arr[2]
    print(bubbleSort(arr))