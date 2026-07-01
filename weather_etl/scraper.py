
# 每个入口文件都需要加这三行，确保 Python 优先从当前文件所在目录查找模块。
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # 确保导入的自己目录下的config.py，而不是其他地方的config.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import config
import logging
import cleaner
# 设置日志展示级别为info，这样 info()、warning()、error() 都会输出  （默认只展示：warning()及之后的级别）
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")  

URL_BASE = config.URL_BASE
HEADERS = config.HEADERS
TIMEOUT = 10                    

def fetch_json(url: str) -> dict:
    """
    请求 city3jdata 接口,返回 dict
    """
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.encoding = 'utf-8'
    return response.json()

def normalize_full_code(prov_code: str, city_url_code: str, county_code: str) -> str:
    """
    直辖市拼接规则：省代码+县代码+00
    普通城市拼接规则：省代码+城市代码+县代码
    """
    DIRECT_PROV_CODES = {"10101", "10102", "10103", "10104"}  # 京沪津渝
    return prov_code+county_code+"00" if prov_code in DIRECT_PROV_CODES else prov_code+city_url_code+county_code
    

def crawl_all_city_codes() -> list[dict]:
    """
    爬取所有城市的代码：省/市/县
    返回: [{"province":"北京","prov_code":"10101",
             "city":"北京","city_code":"1010101",
             "county":"北京","full_code":"101010100"}, ...]
    """
    results = []   # 存储所有城市代码的列表
    provs = fetch_json(f"{URL_BASE}/data/city3jdata/china.html")
    logging.info(f"爬取到 {len(provs)} 个省份数据")

    for provs_code, provs_name  in provs.items():  # items()会把json转为列表
        logging.info(f"爬取省份: {provs_name}，代码: {provs_code}")
        logging.info(f"{URL_BASE}/data/city3jdata/provshi/{provs_code}.html")
        # 二级：城市
        try:
            cities = fetch_json(f"{URL_BASE}/data/city3jdata/provshi/{provs_code}.html")
        except Exception as e:
            logging.error(f"爬取省份数据失败: {provs_name}，错误: {e}")
            continue

        # 三级：县区
        for city_url_code, city_name in cities.items():
            city_code = provs_code + city_url_code  # 城市代码是省代码 + 市代码
            logging.info(f"爬取城市: {city_name}，代码: {city_code}")
            logging.info(f"{URL_BASE}/data/city3jdata/station/{city_code}.html")
            try:
                counties = fetch_json(f"{URL_BASE}/data/city3jdata/station/{city_code}.html")
                # 获取县区数据成功，遍历县区，并将省、市、县信息存入结果列表
                for county_code, county_name in counties.items():
                    # 区分直辖市、普通城市，然后拼接县代码
                    full_code = normalize_full_code(provs_code, city_url_code, county_code)
                    results.append({
                        "province": provs_name,
                        "prov_code": provs_code,
                        "city": city_name, 
                        "city_code": city_code,
                        "county": county_name,
                        "county_code": full_code,    # 县代码是城市代码 + 县代码
                    })
            except Exception as e:  # 实际也没有运行这些代码
                logging.warning(f"{city_name}, {city_code}获取县数据失败")
                continue
        time.sleep(0.15)    # 爬完一个城市后，避免请求过快，给服务器一些缓冲时间
    # print(results)
    return results

# 爬取县的七日天气
def fetch_city_7day_forecast(county_code, county):
    # 构建请求URL
    url = f"{URL_BASE}/weather/{county_code}.shtml"
    logging.info(f"当前正常爬取{county_code}, {county}的天气")
    logging.info(url)
    result = requests.get(url=url, headers=HEADERS)
    # 该站点 charset=GBK / GB2312，用 apparent_encoding 自动识别最稳
    result.encoding = result.apparent_encoding or "utf-8"
    # 解析HTML
    soup = BeautifulSoup(result.text, "html.parser")
    # 天气数据在 <div id="7d"> 里的 <ul class="t clearfix"><li>...</li></ul>
    div_7d = soup.find("div", class_="c7d", id="7d")
    if div_7d is None:
        logging.warning(f"未找到天气数据块，county_code={county_code}，跳过")
        return []
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
        
        # 清洗温度数据
        temp_high = cleaner.clean_temp(temp_high)
        temp_low = cleaner.clean_temp(temp_low)
        

        # 将提取的数据添加到 rows 列表中
        rows.append(
            {
            "county_code": county_code,
            "county":county,
            "date": date,
            "weather": weather,
            "temp_high": temp_high,
            "temp_low": temp_low,
            }
        )
    
    # 处理日期
    date_list = [ row["date"] for row in rows]          # 获取日期列表
    date_list_new = parse_weather_dates(date_list)      # 改正日期列表内的格式
    for row, date_new in zip(rows, date_list_new):      # 新日期弄进rows里面
        row["date"] = date_new

    # 打印结果 & 返回结果
    for row in rows:
        print(row)
    return rows

# 转换日期格式; 30日（今天） -> 2026-6-30
def parse_weather_dates(date_list : list) -> list:
    today = datetime.now()
    result = []
    # enumerate()会给列表加上索引：[(0, "30日（今天）"),  (1, "1日（明天）")]
    for i, date_text in enumerate(date_list):
        # 计算目标日期：按 今天+索引 计算即可
        target_date = today + timedelta(days=i)
        result.append(target_date)
    return result

if __name__ == "__main__":
    url = "http://www.weather.com.cn/data/city3jdata/china.html"
    # results = crawl_all_city_codes()
    # fetch_city_7day_forecast(101010100, "北京")
    # date  = ["30日（今天）", 1, 2]
    # print(parse_weather_dates(date))
    json =  fetch_json(url=url)
    print(json)


