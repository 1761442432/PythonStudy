import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


if __name__=="__main__":
    dirname = os.path.dirname(__file__)
    # 构建 Excel 文件路径（跨平台兼容）
    file_path = os.path.join(dirname,'pandas_stock', 'stock_data_2026_6.xlsx')
    # 读取 Excel 文件到 DataFrame
    data = pd.read_excel(file_path)

    # 设置滚动窗口大小（20 个交易日 ≈ 1 个月）
    window_days = 20
    # 计算滚动 OLS 特征
    data['MA'] = data['Close'].rolling(window_days).mean()
    data['bias'] = data['Close'] / data['MA']
    bias_tail = data['bias'].dropna().iloc[-window_days:]
    score = np.polyfit(np.arange(window_days), bias_tail / bias_tail.iloc[0], 1)[0].real * 10000

    print(data, score)

    # ================= 3. 单图双 Y 轴可视化 =================
    # ================= 1. 环境与字体设置 =================
    # 解决中文显示问题 (Windows: SimHei, Mac: Arial Unicode MS / PingFang HK)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False 

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- 左 Y 轴：绘制 Close 价格 ---
    color1 = 'tab:blue'
    ax1.set_xlabel('交易日 (Index)', fontsize=12)
    ax1.set_ylabel('收盘价 (Close)', color=color1, fontsize=12)
    ax1.plot(data.index, data['Close'], color=color1, label='Close', linewidth=1.5)
    ax1.plot(data.index, data['MA'], color='gray', linestyle='--', label=f'MA{window_days}', linewidth=1)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # --- 右 Y 轴：绘制 Bias 乖离率 ---
    ax2 = ax1.twinx()  # 创建共享 X 轴的第二个 Y 轴
    color2 = 'tab:orange'
    ax2.set_ylabel('乖离率 (Bias)', color=color2, fontsize=12)
    ax2.plot(data.index, data['bias'], color=color2, label='Bias', linewidth=1.5)
    ax2.axhline(y=1.0, color='red', linestyle=':', linewidth=1.5, label='Bias = 1.0 (基准)')
    ax2.tick_params(axis='y', labelcolor=color2)

    # --- 合并图例与标题 ---
    # 获取两个轴的图例句柄和标签，合并显示在顶部
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    plt.title('收盘价 (Close) 与 乖离率 (Bias) 走势对比', fontsize=14, pad=15)
    plt.grid(True, linestyle='--', alpha=0.3, axis='both')
    
    # 自动调整布局并显示
    plt.tight_layout()
    plt.show()

    
