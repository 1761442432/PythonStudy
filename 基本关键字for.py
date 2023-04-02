def myFor():
    arr = []
    for i in range(8):
        arr.append("X")
    return arr
print("方式1（等于方式2）：",myFor())

arr2 = ["X" for i in range(8)]
print("方式2（等于方式1）：", arr2)

# join用法 ：就是把多个字符，合并成一个字符串，并且以“什么字符串”隔开，如：#
print("将列表合并成字符串，并且以#号隔开每个字符：" + "#".join(arr2))