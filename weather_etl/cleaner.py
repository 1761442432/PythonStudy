import pandas as pd

# 将 list of dict 格式 转换为：DataFrame 格式
def listDict_to_dataFrame(results : list) -> pd.DataFrame:
    df = pd.DataFrame(results)
    return df

# 清洗温度：去掉 "℃" 和两端空白
def clean_temp(temp_str: str) -> float:
    if temp_str is None or temp_str=="None":
        return None
    #  去掉 "℃" 和两端空白
    temp_str = temp_str.replace("℃", "").strip()
    return float(temp_str)

if __name__=="__main__":
    print(clean_temp(None))