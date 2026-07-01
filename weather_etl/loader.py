# 每个入口文件都需要加这三行，确保 Python 优先从当前文件所在目录查找模块。
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import config

import pandas as pd
import pymysql
from sqlalchemy import create_engine


# 连接数据库
def init_db() -> pymysql.connect:
    # 建立连接
    conn = pymysql.connect(
    host=config.MYSQL_DB['ip'],                     #   MySQL 地址
    port=config.MYSQL_DB['port'],                   #   端口
    user=config.MYSQL_DB['user'],                   #   用户名
    password=config.MYSQL_DB['password'],           #   密码
    # database="sys",    #   指定数据库
    charset="utf8mb4",          #   字符集
    cursorclass=pymysql.cursors.DictCursor,     #   返回字典（若不写，默认元祖）
    )

    # 连接后立即设置时区为东八区，解决 Windows 下 MySQL NOW() 差8小时的问题
    cursor = conn.cursor()
    cursor.execute(config.MYSQL_DB.get('init_sql', ''))

    return conn

# 创建城市表
def create_db_cities(conn: pymysql.connect) -> bool:
    #  创建游标（执行 SQL 的工具）
    cursor = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS sys.db_cities (
        id          INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
        province    VARCHAR(50)  COMMENT '省份名称',
        prov_code   VARCHAR(20)  COMMENT '省份代码',
        city        VARCHAR(50)  COMMENT '城市名称',
        city_code   VARCHAR(20)  COMMENT '城市代码',
        county      VARCHAR(50)  COMMENT '县名称',
        county_code VARCHAR(20)  UNIQUE COMMENT '县代码',
        crawl_time  DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中国天气网城市表';
    """

    cursor.execute(sql)
    conn.commit()
    return True

# 插入城市数据
def listDict_to_mysql_cities(conn: pymysql.connect, results: list[dict]) -> bool:
    #  创建游标（执行 SQL 的工具）
    cursor = conn.cursor()

    # list[dict] 类型，插入数据库时，需要占位符 %(name)s
    sql = """
    INSERT INTO sys.db_cities
    (province, prov_code, city, city_code, county, county_code)
    VALUES (%(province)s, %(prov_code)s, %(city)s, %(city_code)s, %(county)s, %(county_code)s)
    ON DUPLICATE KEY UPDATE
        province=VALUES(province), city=VALUES(city), city_code=VALUES(city_code),
        county=VALUES(county), prov_code=VALUES(prov_code),county_code=VALUES(county_code),
        crawl_time=NOW()
    """

    cursor.executemany(sql, results)
    conn.commit()
    return True


# 查询 县code
def select_county_code(conn: pymysql.connect) -> list[dict]:
    #  创建游标（执行 SQL 的工具）
    cursor = conn.cursor()

    #查询sql
    sql = """
    select county_code, county from sys.db_cities;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
    # return [ r["county_code"] for r in rows]

# 创建天气表
def create_db_weather(conn: pymysql.connect) -> bool:
    #  创建游标（执行 SQL 的工具）
    cursor = conn.cursor()

    # 创建sql
    sql = """
        CREATE TABLE IF NOT EXISTS sys.db_weather (
        id          INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
        county      VARCHAR(50)  COMMENT '县名称',
        county_code VARCHAR(20)  COMMENT '县代码',
        date    	date         COMMENT '预报日期',
        weather     VARCHAR(100) DEFAULT NULL COMMENT '天气描述',
        temp_high   DOUBLE       DEFAULT NULL COMMENT '最高温(℃)',
        temp_low    DOUBLE       DEFAULT NULL COMMENT '最低温(℃)',
        created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
        UNIQUE KEY uk_city_date (county_code, date) COMMENT '防止同一城市同一天重复插入'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中国天气网7日天气';
    """

    cursor.execute(sql)
    conn.commit()
    return True

def listDict_to_mysql_weather(conn: pymysql.connect, results: list[dict]) -> bool:
    #  创建游标（执行 SQL 的工具）
    cursor = conn.cursor()

    # list[dict] 类型，插入数据库时，需要占位符 %(name)s
    sql = """
    INSERT INTO sys.db_weather
    (county, county_code, date, weather, temp_high, temp_low)
    VALUES (%(county)s, %(county_code)s, %(date)s, %(weather)s, %(temp_high)s, %(temp_low)s)
    ON DUPLICATE KEY UPDATE
        county=VALUES(county), county_code=VALUES(county_code), date=VALUES(date),
        weather=VALUES(weather), temp_high=VALUES(temp_high), temp_low=VALUES(temp_low),
        created_at=NOW()
    """

    cursor.executemany(sql, results)
    conn.commit()
    return True

if __name__=="__main__":
    conn = init_db()
    # rows = select_county_code(conn)
    create_db_weather(conn)
    de = [
        {'county_code': 101340104, 'county': '北京', 'date': '29日（今天）', 'weather': '多云', 'temp_high': None, 'temp_low': None},
        {'county_code': 101340104, 'county': '北京', 'date': '30日（明天）', 'weather': '多云转阴', 'temp_high': 30.0, 'temp_low': 24.0},
        {'county_code': 101340104, 'county': '北京', 'date': '1日（后天）', 'weather': '多云转阴', 'temp_high': 29.0, 'temp_low': 24.0},
        {'county_code': 101340104, 'county': '北京', 'date': '2日（周四）', 'weather': '多云', 'temp_high': 29.0, 'temp_low': 25.0},
        {'county_code': 101340104, 'county': '北京', 'date': '3日（周五）', 'weather': '小雨转晴', 'temp_high': 30.0, 'temp_low': 24.0},
        {'county_code': 101340104, 'county': '北京', 'date': '4日（周六）', 'weather': '多云', 'temp_high': 30.0, 'temp_low': 24.0},
        {'county_code': 101340104, 'county': '北京', 'date': '5日（周日）', 'weather': '多云转阴', 'temp_high': 29.0, 'temp_low': 24.0}
    ]

    listDict_to_mysql_weather(conn=conn, results=de)

