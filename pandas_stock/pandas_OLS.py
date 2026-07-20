# ============================================
# 滚动窗口 OLS 回归分析
# 功能：使用滚动窗口计算股票的每日 OLS 斜率和 R²，
#       衡量价格趋势的方向（斜率）和强度（R²）
# 作者：myZXX
# 日期：2026-07-15
# ============================================

import pandas as pd  # 数据处理
import numpy as np  # 数值计算
import matplotlib.pyplot as plt  # 绘图
import seaborn as sns  # 美化图表
from sklearn.linear_model import LinearRegression  # 线性回归模型
import yfinance as yf  # 雅虎财经数据接口（备用）
import warnings  # 警告控制
import os  # 文件和路径操作

# 忽略警告信息，避免控制台输出干扰
warnings.filterwarnings('ignore')
# 设置 seaborn 主题：白色背景 + 网格线
sns.set_theme(style='whitegrid')
# 设置 matplotlib 中文字体（优先 SimHei，备选 Arial Unicode MS）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
# 解决坐标轴负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


def get_rolling_ols_features(df, window=20):
    '''
    使用滚动窗口计算每天的 OLS 斜率和 R²

    参数:
        df (pd.DataFrame): 必须包含 'Close' 列（收盘价）
        window (int): 滚动窗口大小，默认 20 个交易日

    返回:
        pd.DataFrame: 包含原始收盘价、滚动斜率、滚动 R² 的数据表

    说明:
        - 滚动斜率 (Rolling_Slope): 最近 window 天收盘价的线性趋势斜率，
          正数表示上涨趋势，负数表示下跌趋势
        - 滚动 R² (Rolling_R2): 拟合优度，值越接近 1 表示趋势越线性（越"纯粹"）（上升/下降 趋势明显），
          值越接近 0 表示趋势越杂乱（震荡明显）
    '''
    # 复制收盘价数据，避免修改原始 DataFrame
    data = df[['Close']].copy()  # df[['Close']] 返回DataFrame； df['Close'] 返回Series
    # 创建天数索引（0, 1, 2, ...），作为线性回归的 X 变量
    data['Day_Index'] = np.arange(len(data))  # 用数值 0 1 2 3 作为索引，赋值给 Day_Index

    # --- 定义滚动窗口的自定义计算函数 ---

    def calc_rolling_slope(window_data):
        '''
        计算滚动窗口内的线性回归斜率

        参数:
            window_data (np.array): 窗口内的收盘价序列（长度 = window)

        返回:
            float: 线性回归斜率，表示每日平均价格变化量
                   （正值 = 上涨趋势，负值 = 下跌趋势）
        '''
        # y = 收盘价，raw=True 时已是 numpy 数组
        y = window_data
        # X = 天数索引 [0, 1, 2, ..., window-1]
        X = np.arange(len(y))

        # 如果窗口内数据不足或存在 NaN，返回 NaN（无效值）
        if len(y) < window or np.isnan(y).any():  # np.isnan(y).any() 数组中包含一个以上None返回True， 否则返回False
            return np.nan

        # 拟合线性回归模型，返回斜率
        # model = LinearRegression().fit(X, y)
        # return model.coef_[0]  # coef_[0] 是斜率

        model = get_ols(X, y)
        return model[1]

    def calc_rolling_r2(window_data):
        '''
        计算滚动窗口内线性回归的 R²(拟合优度)

        参数:
            window_data (np.array): 窗口内的收盘价序列

        返回:
            float: R² 值(0~1)，衡量趋势的"线性纯度"
                   - 越接近 1:价格走势越接近直线(强趋势)
                   - 越接近 0:价格走势越杂乱(无趋势或震荡)
        '''
        y = window_data
        X = np.arange(len(y)).reshape(-1, 1)
        # 数据完整性检查
        if len(y) < window or np.isnan(y).any():
            return np.nan
        model = LinearRegression().fit(X, y)
        # score() 返回 R² = 1 - (残差平方和 / 总平方和)
        return model.score(X, y)

    # --- 应用滚动计算 ---
    # rolling(window, min_periods=window)：
    #   - window=20（最大取值）：每次取最近 20 个交易日
    #   - min_periods=window（最小取值，不足时为Nan）：前 window-1 天数据不足，输出 NaN
    #   - .apply(func) ： 取最近20天的值， 计算calc_rolling_slope赋值给Rolling_Slope
    # apply(func, raw=True)：raw=True 将窗口数据作为 numpy 数组传入，性能更好
    # 举例：     
    #   - prices = pd.Series([10, 11, 12, 11.5, 13])
    #   - print(prices.rolling(window=3, min_periods=2).mean())
    #   - 输出：NaN（不足2天） 10.5（前两天平均值） 11.0（前3天的平均值） 11.5（11、12、11.5的平均值） 12.67（12、 11.5、 13的平均值）
    # 说明：
    #   - apply传参（一个数一个数传）： 10   11    12   ... 
    #   - rolling(3, 2).apply传参（一组一组传）： 10   10,11   10,11,12  11,12,11.5  ... 
    data['Rolling_Slope'] = data['Close'].rolling(
        window=window, min_periods=window
    ).apply(calc_rolling_slope, raw=True)

    data['Rolling_R2'] = data['Close'].rolling(
        window=window, min_periods=window
    ).apply(calc_rolling_r2, raw=True)

    return data

# 线性回归函数：复现 statsmodels 的 OLS
# 对 (x, y) 做一元线性回归：y = slope * x + intercept
# 返回值：(intercept, slope, r²)
#   - intercept: 截距
#   - slope: 斜率（RSRS中的支撑/阻力强度）
#   - r²: 拟合优度（0~1，越接近1线性关系越强）
def get_ols(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    # r² = 1 - (残差平方和 / 总平方和)
    r2 = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return (intercept, slope, r2)


# ================= 主程序入口 =================
if __name__ == '__main__':
    # --- 备选方案：从 yfinance 直接拉取数据（已注释） ---
    # # 获取最近 2 年的数据
    # df = yf.download('510300.SS', period='2y', progress=False)
    # # yfinance 返回 MultiIndex 列名，取第一层
    # if isinstance(df.columns, pd.MultiIndex):
    #     df.columns = df.columns.get_level_values(0)
    # df = df[['Close']].dropna()

    # --- 从本地 Excel 文件读取数据 ---
    # __file__ 是当前脚本的完整路径
    # dirname 获取脚本所在目录: ..\PythonStudy\pandas_stock
    dirname = os.path.dirname(__file__)
    # 构建 Excel 文件路径（跨平台兼容）
    file_path = os.path.join(dirname, 'stock_data_2026_6.xlsx')
    # 读取 Excel 文件到 DataFrame
    df = pd.read_excel(file_path)

    # 设置滚动窗口大小（20 个交易日 ≈ 1 个月）
    window_days = 20
    # 计算滚动 OLS 特征
    result_df = get_rolling_ols_features(df, window=window_days)

    # --- 打印最近 5 天的结果 ---
    print(f'\n--- 最近 5 天的动态 OLS 参数 (窗口={window_days}天) ---')
    print(result_df[['Close', 'Rolling_Slope', 'Rolling_R2']].tail())

    # ================= 可视化 =================
    # 创建 2 行 1 列的子图，共享 X 轴（日期）
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # ---------- 图 1: 收盘价 vs 滚动斜率 ----------
    # 主坐标轴：绘制收盘价曲线
    ax1.plot(result_df.index, result_df['Close'],
             label='收盘价', color='#1f77b4', alpha=0.7)
    # 次坐标轴：绘制滚动斜率（因为斜率和价格量级不同）
    ax1_twin = ax1.twinx()
    ax1_twin.plot(result_df.index, result_df['Rolling_Slope'],
                  label=f'{window_days}日滚动斜率 (动量)',
                  color='#d62728', linewidth=1.5)
    # 零轴参考线：斜率 > 0 为上涨趋势，< 0 为下跌趋势
    ax1_twin.axhline(0, color='black', linestyle='--', linewidth=1)

    ax1.set_title('股票价格 vs 每日动态滚动斜率 (Rolling Slope)',
                  fontsize=14, fontweight='bold')
    ax1.set_ylabel('价格')
    ax1_twin.set_ylabel('滚动斜率 (每日平均变化量)')

    # ---------- 图 2: 滚动 R²（拟合优度） ----------
    ax2.plot(result_df.index, result_df['Rolling_R2'],
             label=f'{window_days}日滚动 R²', color='#2ca02c', linewidth=1.5)
    # R² = 0.5 参考线：高于此值表示趋势较明显
    ax2.axhline(0.5, color='orange', linestyle='--',
                label='R² = 0.5 (趋势强弱分界线)')
    ax2.set_ylabel('R² (0~1)')
    ax2.set_xlabel('日期')
    ax2.set_title('每日动态拟合优度 (R²): 衡量当前趋势的"线性纯度"',
                  fontsize=12)

    # --- 合并图例 ---
    # 图 1 有主、次两个坐标轴，需要合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax2.legend(loc='upper left')

    # 日期标签旋转 45 度，避免重叠
    plt.xticks(rotation=45)
    # 自动调整子图间距
    plt.tight_layout()
    # 显示图表
    plt.show()