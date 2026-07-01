import requests
from bs4 import BeautifulSoup

def fetch_city_7day_forecast(city_id, city_name):
    # 模拟浏览器请求头，避免被反爬虫机制阻止
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.weather.com.cn/",
    }
    # 构建请求URL
    url = f"http://www.weather.com.cn/weather/{city_id}.shtml"
    result = requests.get(url=url, headers=HEADERS)
    # 该站点 charset=GBK / GB2312，用 apparent_encoding 自动识别最稳
    result.encoding = result.apparent_encoding or "utf-8"
    # 解析HTML
    soup = BeautifulSoup(result.text, "html.parser")
    # 天气数据在 <div id="7d"> 里的 <ul class="t clearfix"><li>...</li></ul>
    div_7d = soup.find("div", class_="c7d", id="7d")
    t_clearfix_lis = div_7d.find("ul", class_="t clearfix").find_all("li")
    # 提取天气数据
    rows = []
    for li in t_clearfix_lis:
        # 提取每一天的天气信息
        # strip() 方法，去除首尾的所有空白字符（空格、\n、\r、\t 等），只保留中间的有效内容
        date = li.find("h1").text.strip()  # 日期
        weather = li.find("p", class_="wea").text.strip()  # 天气
        try:
            # 获取 tem 下的 span/i 标签，分别是最高温度和最低温度
            temp_high = li.find("p", class_="tem").find("span").text.strip()  # 最高温度
            temp_low = li.find("p", class_="tem").find("i").text.strip()  # 最低温度
        except AttributeError:
            # 有些天气预报可能没有最高温度或最低温度，设置为 None
            temp_high = temp_low = None
        # 将提取的数据添加到 rows 列表中
        rows.append(
            {
            "城市": city_name,
            "城市代码": city_id,
            "日期": date,
            "天气": weather,
            "最高温(℃)": temp_high,
            "最低温(℃)": temp_low,
        }
        )
    # 打印结果
    for row in rows:
        print(row)
    return rows

import os
import pandas as pd
# 将数据保存到 Excel 文件
def into_excel(rows):
    # 拼接文件路径，不存在文件时，会自动创建
    OUTPUT_DIR = os.path.dirname(__file__)   # 保存到脚本所在目录
    filename = "中国天气网_城市天气预报.xlsx"
    filename = os.path.join(OUTPUT_DIR, filename)
    # 将数据转换为 DataFrame，并保存到 Excel 文件
    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"数据已保存到 {filename}")

# 将日期字符串转换为 datetime 对象，方便后续处理
# 将 '11日（今天）' 转成 '2026-06-11
def parse_date(date_str):
    # 获取代码运行时的当前系统日期时间（例如今天 2026-06-16）
    today = datetime.now()
    # 以 "日" 为分隔符切割字符串，取第一部分（如 "11日（今天）" → "11"）
    # 将切割后的字符串转换为整数，得到日期（如 "11" → 11）
    day = int(date_str.split("日")[0])
    # 简化处理：假设是同一个月，如果日期小于当前日期，说明是下个月
    # today.day 获取当前日期的日部分（例如 16），与提取的日期进行比较
    if day < today.day:
        today += timedelta(days=30)      # 简单地加30天，跨月处理
    else:
        today = today.replace(day=day)   # 同月，直接替换日期
    return today.date()  # 返回日期部分，去掉时间

# 清洗温度数据（去掉 ℃）
def clean_temp(temp_str):
    if temp_str is None:
        return None  # 如果温度字符串为 None，直接返回 None
    # 将温度字符串转换为整数，去掉 "℃" 符号
    temp_str = str(temp_str).replace("℃", "").strip()  # 去掉 "℃" 和两端空白
    try:
        return float(temp_str)  # 转换为浮点数
    except ValueError:
        return None  # 如果转换失败，返回 None

import pymysql
from sqlalchemy import create_engine
from datetime import datetime, timedelta
# 连接数据库，创建表格，插入数据的代码
def into_sql(rows):
    # 指定数据库：sys（必须指定）
    engine = create_engine(
       "mysql+pymysql://root:123456@localhost:3306/sys?charset=utf8mb4"
       )
    df = pd.DataFrame(rows)

    # 重命名列：columns={'旧列名': '新列名'}：指定要重命名的列和新的列名
    # inplace=True：原地修改，不返回新的 DataFrame
    df.rename(
        columns={
            "城市": "city_name",
            "城市代码": "city_id",
            "日期": "date",
            "天气": "weather",
            "最高温(℃)": "high_temp",
            "最低温(℃)": "low_temp",
        },
        inplace=True,
    )

    # 将日期列转换为标准日期格式，方便后续查询和分析
    # 选取 date 列，使用 apply 方法对每个元素应用 parse_date 函数，将字符串转换为日期对象
    df["date"] = df["date"].apply(parse_date)

    # 温度列转换为浮点数，去掉 "℃" 符号，方便数值计算
    df["high_temp"] = df["high_temp"].apply(clean_temp)
    df["low_temp"] = df["low_temp"].apply(clean_temp)

    # 将数据写入 MySQL 数据库，表名为 weather
    df.to_sql(
        name="weather",    # 表名
        con=engine,
        index=False,  # 不把索引写进数据库
        # fail    表存在就报错（默认）
        # replace 删除旧表，新建（首次运行或表结构变化时使用）
        # append  追加数据（表结构一致时最常用）
        if_exists="append"
    )
    print(df)

if __name__ == "__main__":
    city_id = "101010100"  # 北京市的城市ID
    city_name = "北京"
    rows = fetch_city_7day_forecast(city_id, city_name)
    into_excel(rows)
    into_sql(rows)