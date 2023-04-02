
# 插入排序：也是一种从小到大(从大到小)排序
# 找出最小的数，插入为列表第1个位置
# 然后找出第2小的数，插入为列表第2个位置
# 依次后面的数，一直插入，知道列表排序完成
def insertionSort(arr):
    for i in range(len(arr)):
        index = i
        # and index-1 >= 0 是为了防止：索引越界异常、
        # 当 arr[index-1] > arr[index] 成立，如：第1个比第2个数大时，
        while arr[index-1] > arr[index] and index-1 >= 0:
            # arr[index-1] 与 arr[index] 互换位置，如：第1个 与 第2个数互换位置
            arr[index], arr[index-1] = arr[index-1], arr[index]
            # 这一步是为了继续与前面已经排序好的数比较，看看谁大1
            index -= 1
    return arr

if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6]
    print("排序后的数组:",insertionSort(arr))
