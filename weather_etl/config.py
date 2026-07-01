URL_BASE = "https://www.weather.com.cn"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0.0.0 Safari/537.36",
    "Referer": "http://www.weather.com.cn/",
}

MYSQL_DB = {
    "user":"root",
    "password":"123456",
    "ip":"localhost",
    "port": 3306,
    "init_sql": "SET time_zone = '+08:00'",   # 显式设置东八区，解决 Windows 下 MySQL 时区差8小时的问题
}