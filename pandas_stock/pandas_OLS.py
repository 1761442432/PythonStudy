
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import yfinance as yf
import warnings


# 忽略 yfinance 可能产生的警告
warnings.filterwarnings('ignore')

# 设置绘图风格和中文字体，防止图表中文乱码
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 兼容 Windows 和 Mac
plt.rcParams['axes.unicode_minus'] = False

def ols_fit_and_plot(df, window_days=None):
    """
    使用最小二乘法对时间序列进行拟合并可视化
    """
    # 1. 数据预处理 (ETL)
    # 线性回归需要数值型特征，我们将日期转换为从 0 开始的整数序列 (0, 1, 2, ...)
    data = df.copy()
    data['Date'] = np.arange(len(data))
    
    # 如果指定了窗口，则只取最近 N 天（模拟量化中的滚动窗口）
    if window_days:
        data = data.tail(window_days)
        
    X = data['Date'].values.reshape(-1, 1) # sklearn 要求 X 是二维数组
    y = data['Close'].values

    # 2. 模型训练 (Modeling)
    # 使用 scikit-learn 的 LinearRegression，其底层即为普通最小二乘法 (OLS)
    model = LinearRegression()
    model.fit(X, y)
    
    # 提取 OLS 参数
    slope = model.coef_[0]      # 斜率 (每日平均变化量)
    intercept = model.intercept_ # 截距
    r_squared = model.score(X, y) # 决定系数 R² (拟合优度)
    
    # 生成拟合直线的预测值
    data['Fitted_Close'] = model.predict(X)

    # 3. 可视化 (Visualization)
    plt.figure(figsize=(12, 6))
    
    # 绘制原始收盘价
    plt.plot(data.index, data['Close'], label='实际收盘价 (Close)', color='#1f77b4', linewidth=1.5)
    
    # 绘制 OLS 拟合直线
    plt.plot(data.index, data['Fitted_Close'], label=f'OLS 拟合直线 (R² = {r_squared:.4f})', 
             color='#ff7f0e', linewidth=2.5, linestyle='--')
    
    # 图表装饰
    title_suffix = f" (最近 {window_days} 个交易日)" if window_days else " (全周期)"
    plt.title(f'股票时间序列的最小二乘法 (OLS) 线性拟合{title_suffix}', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('价格', fontsize=12)
    plt.legend(loc='upper left', fontsize=11)
    plt.xticks(rotation=45)
    
    # 在图表上添加拟合公式文本框
    formula_text = f"拟合公式: y = {slope:.4f} * x + {intercept:.4f}\n斜率 (日均趋势): {slope:.4f}\nR² (解释方差比例): {r_squared:.4f}"
    plt.gca().text(0.02, 0.95, formula_text, transform=plt.gca().transAxes, 
                   fontsize=11, verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    plt.show()
    
    return slope, intercept, r_squared

if __name__ == "__main__":
        # 获取数据 (以沪深300ETF为例，周期1年)
    # 注意: 510300.SS 是 yfinance 中沪深300ETF的代码
    # stock_data = get_stock_data(ticker="510300.SS", period="1y")
    # print("\n--- 数据预览 ---")
    # print(stock_data.tail())

    # 读取文件
    path = os.path.dirname(__file__)
    path_file = os.path.join(path, "stock_data_2026_6.xlsx")

    # -------------------- 图标显示， 多个指标汇总 -----------------
    # index_col=0 第0列为索引； parse_dates=True 自动尝试解析所有看起来像日期的列为 datetime 类型
    df = pd.read_excel(path_file, index_col=0, parse_dates=True) 


    ols_fit_and_plot(df=df)


