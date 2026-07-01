# -*- coding: utf-8 -*-
"""
天气数据 ETL 主入口模块

功能说明：
    1. 爬取所有城市的天气数据，并将其写入 MySQL 数据库。
    2. （可选）遍历每个县/区，爬取未来 7 天的天气预报并入库。

运行方式：
    python main.py

依赖模块：
    - scraper:   负责从天气网站抓取数据
    - cleaner:   负责清洗和格式化原始数据
    - loader:    负责数据库的连接与读写操作
"""

import sys
import os
import time

# 将当前脚本所在的目录插入到 sys.path 的最前面
# os.path.dirname(__file__) 获取当前文件的绝对目录路径
sys.path.insert(0, os.path.dirname(__file__))

import cleaner as cl        # 数据清洗模块（如去空格、格式转换等）
import scraper as sc        # 数据爬取模块（HTTP 请求、HTML 解析等）
import loader as lo         # 数据加载模块（数据库连接、建表、写入等）

# ============================================================
# 2. 爬取城市数据，并写入数据库
# ============================================================
# 2.1 初始化数据库连接
conn = lo.init_db()
# # 2.2 调用爬虫，获取所有城市的基础信息（城市编码、城市名称等）
results = sc.crawl_all_city_codes()
# # 2.3 如果城市表不存在则创建
lo.create_db_cities(conn=conn)
# # 2.4 将城市数据批量写入 MySQL 数据库
lo.listDict_to_mysql_cities(conn=conn, results=results)

# ============================================================
# 3. 爬取每个县的天气数据，并写入数据库（当前已注释，按需启用）
# ============================================================
# 3.1 从数据库中查询出所有县/区的编码
county_rows = lo.select_county_code(conn)
# 3.2 如果天气表不存在则创建
lo.create_db_weather(conn)
# 3.3 遍历每个县/区，爬取未来 7 天的天气预报
for cr in county_rows:
    # 根据县编码和县名爬取天气数据
    results = sc.fetch_city_7day_forecast(
        county_code=cr["county_code"],
        county=cr["county"]
    )
    # 将爬取结果写入天气表
    lo.listDict_to_mysql_weather(conn=conn, results=results)
    # 休眠 0.15 秒，避免请求频率过高被封 IP（给服务器缓冲时间）
    time.sleep(0.15)