
def feibo():
    """
    斐波那契数列：第1、2个元素=1，第3个元素开始，是前面2个数的和
    :return:
    """
    arr =[]
    for i in range(10):
        if i ==0 or i ==1:                      # 第1、2个元素=1
            arr.append(1)
        else:
            arr.append(arr[i-2]+arr[i-1])       # 第3个元素开始：是前面2个元素的和
    print (arr)

if __name__ == '__main__':
    feibo()