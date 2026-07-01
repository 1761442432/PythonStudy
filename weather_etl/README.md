weather_etl/
├── config.py      # 存放 DB_CONFIG, URL, FILE_PATH
├── scraper.py     # 负责 requests 爬取，返回 JSON/Dict
├── cleaner.py     # 负责 pandas 清洗，返回 DataFrame
├── loader.py      # 负责 sqlalchemy/pymysql 入库
└── main.py        # 串联流程：scraper -> cleaner -> loader
