
# 完整for循环
for num in [1,2,3]:
    print("for循环：",num)
    if num == 2:
        # 退出循环
        break
# 如果for循环通过break跳出，则不执行else。否则会执行
else:
    print("如果for循环通过break跳出，则不执行else。否则会执行")