import datetime

def compare_time2(str_time):
    # 将字符串时间转换为datetime对象
    time_obj = datetime.datetime.strptime(str_time, '%Y-%m-%d')
    # 获取当前时间
    now = datetime.datetime.now()
    # 判断哪个时间更大
    if time_obj > now:
        print('输入的时间更大')
    else:
        print('当前时间更大',str(time_obj))


def compare_time():
    # 获取当前时间
    now = datetime.datetime.now()
    # 将当前时间转换为年月日字符串格式
    now_str = now.strftime('%Y-%m-%d')
    print('当前时间为：', now_str)
    # 将转换的后的时间，加上7天得到一个新的时间
    new_time = now + datetime.timedelta(days=7)
    new_time_str = new_time.strftime('%Y-%m-%d')
    print('加上7天后的时间为：', new_time_str)
    # 将新的时间与当前时间判断谁更大
    if new_time > now:
        print('加上7天后的时间更大')
    else:
        print('当前时间更大')


if __name__ == '__main__':

    compare_time()
    compare_time2('2022-01-01')

    # 获取当前时间
    now = datetime.date.today()
    print('当前时间为：', now)

    # 将当前时间加上40天
    new_time = now + datetime.timedelta(days=40)
    print('加上40天后的时间为：', new_time)