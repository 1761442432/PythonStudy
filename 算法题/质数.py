#质数：除1 和 他本身 外，不能被其他数整除的数
list1=[]
for i in range(2,101):          #先定义被除数的范围
    for j in range(2,i):        #定义除数的范围
        if i%j==0:              # 如果 i%j取余==0，则说明这不是质数。j：表示 2 -- (i-1)
            break
    else:
        list1.append(i)
print(list1)