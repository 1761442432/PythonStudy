import random, string
# 随机生成手机号:
def randomMobile():
    print("132" + "".join(random.choice(string.digits) for i in range(8)))
randomMobile()
