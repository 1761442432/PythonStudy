#水仙花：个位立方+十位立方+百位立方=自己
def daffodil():
    for i in range(100, 1000):
        ge = i % 10                 #求出个位
        shi = i / 10 % 10           #求出十位
        bai = i / 100 % 10          #求出百位
        if (ge*ge*ge + shi*shi*shi + bai*bai*bai) == i:
            print(i)                #不知道为啥，没有输出结果？？？
daffodil()