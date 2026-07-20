# ==================== 策略说明 ====================
# 克隆自聚宽文章：https://www.joinquant.com/post/42435
# 标题：最新优化ETF轮动，年化70%加
# 作者：Funine
#
# 克隆自聚宽文章：https://www.joinquant.com/post/40925
# 标题：多因子宽基ETF择时轮动-高收益大资金低回撤
# 作者：养家大哥
#
# 标题：ETF动量轮动RSRS择时-V4.0，2022/8/12
# 作者：养家大哥
#
# 标题：动量ETF轮动RSRS择时-v4
# 作者：杨德勇
#
# ==================== 核心思路 ====================
# v2 养家大哥的思路：
# 趋势因子的特点是无法及时判断趋势的变向，往往趋势变向一段时间后才能跟上，
# 巨大回撤往往就发生在这种时候。因此基于动量因子的一阶导数，衡量趋势的潜在变化速度，
# 若变化速度过快则空仓，反之则按原计划操作。
# 可以进一步发散，衡量动量因子的二阶导、三阶导等等，暂时只测试过一阶导，就是目前这个升级2版本。
#
# ==================== 策略框架 ====================
# 1. initialize()        - 初始化：设定参数、股票池、定时任务
# 2. my_trade_prepare()  - 每日7:00：计算动量排名 + RSRS择时信号
# 3. my_trade()          - 每日9:30：根据信号执行买入/卖出
# 4. my_sell2buy()       - 每日9:32：调仓时的买入操作
# 5. hold_check()        - 每日11:00：盘中止损检查


# ==================== 导入库 ====================
from jqdata import *                   # 聚宽数据接口（attribute_history、get_current_data 等）
import numpy as np                      # 数值计算（polyfit、数组操作）
from jqlib.technical_analysis import *  # 技术分析指标库（WR 威廉指标等）

# ==================== 初始化函数 ====================
# 在回测/实盘开始时调用一次，完成以下配置：
#   1. 基准、滑点、手续费等交易环境设置
#   2. 定义股票池和策略参数
#   3. 预加载历史数据（slope、动量），避免首日数据不足
#   4. 注册定时任务（择时、交易、止损）
def initialize(context):
    # --- 交易环境设置 ---
    set_benchmark('510300.XSHG')        # 基准：沪深300ETF，用于计算超额收益
    set_option('use_real_price', True)   # 使用真实价格交易（非复权价）
    set_option("avoid_future_data", True)  # 避免引入未来数据（防止回测失真）
    set_slippage(FixedSlippage(0.00))    # 滑点：0（ETF流动性好，可设为0）
    # 手续费设置：ETF买卖佣金万分之一，无印花税
    set_order_cost(OrderCost(open_tax=0, close_tax=0.000, open_commission=0.0001, close_commission=0.0001, close_today_commission=0, min_commission=0),
                   type='fund')
    # --- 股票池：宽基ETF ---
    g.stock_pool = [
        '510050.XSHG',  # 上证50ETF（大盘蓝筹）
        '510300.XSHG',  # 沪深300ETF（大盘代表）
        '159949.XSHE',  # 创业板50（成长风格）
        '510500.XSHG',  # 500ETF（中盘股）
        '159915.XSHE',  # 创业板ETF（成长风格）
        '510880.XSHG',  # 红利ETF（价值风格）
        '159901.XSHE',  # 深证100ETF（深市大盘）
        '588000.XSHG',  # 科创50ETF（科技成长）
        '512100.XSHG',  # 中证1000ETF（小盘股）
    ]
    # 备选池：用流动性和市值更大的50ETF分别代替宽指ETF，500与300ETF保留一个

    # --- 策略参数 ---
    g.stock_num = 1            # 每次买入评分最高的前N只股票（本策略只买1只）
    g.momentum_day = 20        # 动量计算窗口：最近20个交易日
    g.ref_stock = '000300.XSHG'  # 择时基准：沪深300指数，用于RSRS计算

    # RSRS（阻力支撑相对强度）参数
    g.N = 18       # 斜率/拟合度计算窗口：最近18天的high-low线性回归
    g.M = 900      # Z-score标准化窗口：用最近900天的slope计算均值和标准差
    g.K = 8        # Z-score斜率窗口：最近8个Z-score值的线性回归斜率

    # 动量参数
    g.biasN = 90            # 乖离动量窗口：相对90日均线的乖离率
    g.lossN = 20            # 止损均线窗口：60分钟K线的MA20
    g.lossFactor = 1.005    # 止损比例：当前价 < 昨收 * 1.005 时触发
    g.SwitchFactor = 1.04   # 换仓阈值：新标的得分 > 当前持仓得分 * 1.04 时换仓

    # 动量一阶导数风控参数
    g.Motion_1diff = 19     # 动量变化速度门限：超过则空仓（防止急涨急跌）
    g.raiser_thr = 4.8      # 单日涨幅门限：超过则空仓（防止追高）

    # RSRS择时阈值
    g.hold_stock = 'null'           # 当前持仓股票代码（用于换仓加分）
    g.score_thr = -0.68             # RSRS买入阈值：Z-score > 此值时买入
    g.score_fall_thr = -0.43        # RSRS下跌卖出阈值：下跌趋势中Z-score < 此值时卖出
    g.idex_slope_raise_thr = 12     # 大盘强势斜率门限：slope > 此值视为强势

    # --- 预加载历史数据 ---
    # 用回测前的历史数据初始化slope序列和动量序列，避免首日数据不足导致NaN
    g.slope_series, g.rsrs_score_history = initial_slope_series()
    g.stock_motion = initial_stock_motion(g.stock_pool)
    
    # --- 注册定时任务（按时间顺序执行） ---
    # 7:00  盘前准备：计算动量排名 + RSRS择时信号，确定今日操作标的和方向
    run_daily(my_trade_prepare, time='7:00', reference_security='000300.XSHG')
    # 9:30  开盘：执行卖出操作（清仓/止损），或全仓买入
    run_daily(my_trade, time='9:30', reference_security='000300.XSHG')
    # 9:32  调仓买入：卖出旧标的后，用90%资金买入新标的（CHANGE信号时）
    run_daily(my_sell2buy, time='9:32', reference_security='000300.XSHG')
    # 11:00 盘中止损：检查60分钟K线是否跌破MA20，触发则清仓
    run_daily(hold_check, time='11:00')

# ==================== 初始化辅助函数 ====================
# 预加载RSRS所需的slope和Z-score序列
# 目的：回测第一天就需要用到大量历史slope数据来计算Z-score，
#       如果不预加载，首日数据不足会导致NaN，影响择时判断
#
# RSRS计算流程：
#   1. 对最近N天的(low, high)做线性回归 → 得到slope（斜率）和r²（拟合度）
#   2. 对最近M天的slope序列做Z-score标准化 → rsrs_score = Z-score × r²
#   3. 对最近K天的rsrs_score做线性回归斜率 → rsrs_slope（趋势方向）
#
# 参数关系：需要预加载的数据量 = N + M + K 天
def initial_slope_series():
    length = g.N + g.M + g.K          # 总共需要的历史天数（18+900+8=926天）
    # 获取沪深300指数的high/low/close数据
    data = attribute_history(g.ref_stock, length, '1d', ['high', 'low', 'close'])
    # 对每N天窗口做OLS回归：low→high 的线性关系，得到(intercept, slope, r²)
    multe_data = [get_ols(data.low[i:i+g.N], data.high[i:i+g.N]) for i in range(length-g.N)]
    slopes = [i[1] for i in multe_data]  # 提取所有slope值
    r2s = [i[2] for i in multe_data]     # 提取所有r²值
    # 计算最近K天的rsrs_score = Z-score × r²
    zscores = [(get_zscore(slopes[i+1:i+1+g.M]) * r2s[i+g.M]) for i in range(g.K)]
    return (slopes, zscores)
    
    
# 预加载各ETF的动量因子序列
# 目的：与initial_slope_series类似，避免回测首日动量数据为空
# 动量计算方法：乖离动量（Bias Momentum）
#   1. 计算收盘价相对90日均线的乖离率 bias = price / MA90
#   2. 对最近20天的乖离率做线性回归，斜率 × 10000 作为动量得分
#   3. 得分越高 → 近期趋势越强 → 优先买入
def initial_stock_motion(stock_pool):
    stock_motion = {}
    for stock in stock_pool:
        motion_que = []
        # 多取1天数据，然后去掉最后一天（避免使用回测当天数据）
        data = attribute_history(stock, g.biasN + g.momentum_day + 1, '1d', ['close'])
        data = data[:-1]  # 去掉最后一天，只用回测前的历史数据
        # 乖离因子 = 收盘价 / 90日均线，取最近momentum_day天
        bias = (data.close / data.close.rolling(g.biasN).mean())[-g.momentum_day:]
        # 线性拟合：对乖离率序列做一元线性回归，斜率×10000作为动量得分
        score = np.polyfit(np.arange(g.momentum_day), bias/bias[0], 1)[0].real * 10000
        motion_que.append(score)
        stock_motion[stock] = motion_que
    return(stock_motion)

# ==================== 择时信号主函数 ====================
# 每日7:00盘前调用，完成以下任务：
#   1. 计算所有ETF的动量排名（get_rank）
#   2. 获取RSRS择时信号（get_timing_signal）→ BUY / SELL
#   3. 根据信号选择目标ETF（排除QDII基金）
#   4. 动量一阶导数风控：若动量变化过快或单日涨幅过大 → 强制SELL
#   5. 确定最终操作信号：BUY（买入）/ SELL（清仓）/ CHANGE（换仓）/ HOLD（持有）
def my_trade_prepare(context):
    hour = context.current_dt.hour
    minute = context.current_dt.minute
    # QDII基金列表：这些是海外ETF，不需要择时（直接用BUY信号）
    out_list = ['513100.XSHG', '511880.XSHG', '513500.XSHG']
    # --- Step 1: 获取动量排名和RSRS择时信号 ---
    rank_list = get_rank(context, g.stock_pool)               # 按动量得分降序排列
    g.timing_signal = get_timing_signal(context, g.ref_stock) # RSRS择时：BUY 或 SELL

    # --- Step 2: 根据择时信号选择目标ETF ---
    # 默认选动量排名第一的ETF
    g.check_out_list = rank_list[0]
    if g.timing_signal == "BUY":
        # 买入信号：优先选A股ETF（跳过QDII海外基金）
        for i in range(len(rank_list)):
            if rank_list[i][0] in out_list:
                continue  # 跳过QDII
            else:
                g.check_out_list = rank_list[i]
                break
    else:
        # 卖出信号：如果持仓的是QDII，则选QDII（不对其择时）
        for i in range(len(rank_list)):
            if rank_list[i][0] in out_list:
                g.check_out_list = rank_list[i]
                break

    # QDII基金不做择时，强制设为BUY（一直持有）
    if g.check_out_list[0] in out_list:
        g.timing_signal = "BUY"

    # --- Step 3: 动量一阶导数风控 ---
    # 核心思想：如果动量变化速度过快（一阶导数过大），说明趋势可能急转，提前空仓避险
    loginfo = "\n" + g.check_out_list[0] + ": " + get_security_info(g.check_out_list[0]).display_name
    loginfo += "\n大盘择时：" + g.timing_signal
    cur_stock = g.check_out_list[0]
    cur_adr = g.check_out_list[2]  # 当日涨跌幅（%）
    # 动量变化速度 = 今日动量 - 昨日动量（一阶导数）
    change_rate = g.stock_motion[cur_stock][-1] - g.stock_motion[cur_stock][-2]
    log.info("涨跌比例:%f, 动量变化速度:%f" % (cur_adr, change_rate))
    loginfo += "\n动量择时："
    # 如果动量变化过快 或 单日涨幅过大 → 强制卖出（防止追高被套）
    if (change_rate > g.Motion_1diff) or (cur_adr > g.raiser_thr):
        g.timing_signal = 'SELL'
        log.info("由于涨跌:%f, 动量变化%0f，今日空仓" % (cur_adr, change_rate))
        loginfo += 'SELL'
    else:
        loginfo += 'BUY'

    # --- Step 4: 确定最终操作信号 ---
    if g.timing_signal == 'SELL':
        # SELL：清仓所有持仓
        for stock in context.portfolio.positions:
            log.info("准备卖出ETF [%s]" % stock)
            send_message("准备卖出ETF [%s]" % stock)
    elif g.timing_signal == 'BUY':
        if g.check_out_list[0] not in context.portfolio.positions:
            if len(context.portfolio.positions) > 0:
                # 持仓有ETF但不是目标ETF → 换仓（先卖后买）
                stock_tmps = list(context.portfolio.positions.keys())
                g.timing_signal = 'CHANGE'  # 改为CHANGE信号，9:32时执行买入
                log.info("准备卖ETF [%s], 买入ETF [%s]" % (stock_tmps[0], g.check_out_list[0]))
                send_message("准备卖ETF [%s], 买入ETF [%s]" % (stock_tmps[0], g.check_out_list[0]))
            else:
                # 空仓 → 直接买入
                log.info("准备买入ETF [%s]" % g.check_out_list[0])
                send_message("准备买入ETF [%s]" % g.check_out_list[0])
    else:
        # HOLD：保持原仓位不动
        send_message("保持原来仓位")
        pass
    log.info(loginfo + '\n今日自选及择时信号:{} {}'.format(g.check_out_list[0], g.timing_signal))
    send_message(loginfo + '\n今日自选及择时信号:{} {}'.format(g.check_out_list[0], g.timing_signal))


# ==================== 止损函数 ====================
# 每日11:00盘中调用，检查是否需要止损
# 止损条件（同时满足）：
#   1. 60分钟K线收盘价 < MA20（均线跌破）
#   2. 当前价格 < 昨日收盘价 × lossFactor（价格下跌）
#
# 止损逻辑：
#   - 先检查目标ETF（zhisun_check）：仅预警，不执行
#   - 再检查持仓ETF（hold_check）：满足条件则清仓
def hold_check(context):
    current_data = get_current_data()
    zhisun_check(context)  # 检查目标ETF是否触发止损（仅预警）
    # 遍历所有持仓，逐一检查止损条件
    if context.portfolio.positions:
        for stk in context.portfolio.positions:
            yesterday_di = attribute_history(stk, 1, '1d', ['close'])  # 昨日收盘价
            dt = attribute_history(stk, g.lossN+2, '60m', ['close'])   # 60分钟K线数据
            # man = 当前价 / MA20，< 1.0 表示跌破均线
            dt['man'] = dt.close / dt.close.rolling(g.lossN).mean()
            # 止损条件：跌破MA20 且 当前价 < 昨收 × 1.005
            if (dt.man[-1] < 1.0) and (current_data[stk].last_price * g.lossFactor <= yesterday_di['close'][-1]):
                stk_dict = context.portfolio.positions[stk]
                if stk_dict.closeable_amount:
                    log.info('准备平仓，总仓位:{}, 可卖出：{}, '.format(stk_dict.total_amount, stk_dict.closeable_amount))
                    send_message("盘中止损，卖出：{}".format(stk))
                    order_target_value(stk, 0)  # 清仓
                else:
                    log.info('无法止损', stk)
                    send_message("无法止损:{}".format(stk))

# 目标ETF止损预警（仅打印日志，不执行卖出）
# 用于监控目标ETF是否也触发了止损条件，辅助决策
def zhisun_check(context):
    current_data = get_current_data()
    stk = g.check_out_list[0]
    yesterday_di = attribute_history(stk, 1, '1d', ['close'])
    dt = attribute_history(stk, g.lossN+2, '60m', ['close'])
    dt['man'] = dt.close / dt.close.rolling(g.lossN).mean()
    if (dt.man[-1] < 1.0) and (current_data[stk].last_price * g.lossFactor <= yesterday_di['close'][-1]):
        log.info("触发止损")
        send_message("触发止损")

# ==================== 交易函数 ====================
# 每日9:30开盘时调用，根据timing_signal执行买卖
# 信号含义：
#   - SELL：清仓所有持仓
#   - CHANGE：先卖出旧标的（9:30），再买入新标的（9:32）
#   - BUY：全仓买入目标ETF
def my_trade(context):
    security = g.check_out_list[0]  # 目标ETF代码
    # 获取当前持仓（如果有）
    c_security = ""
    if len(context.portfolio.positions) > 0:
        stock_tmps = list(context.portfolio.positions.keys())
        c_security = stock_tmps[0]  # 当前唯一持仓

    # SELL 或 CHANGE：卖出当前持仓
    if g.timing_signal == "SELL" or g.timing_signal == "CHANGE":
        if len(c_security) > 0:
            order_target_value(c_security, 0)  # 清仓
            log.info("卖出ETF [%s]" % c_security)

    # BUY：全仓买入目标ETF
    elif g.timing_signal == "BUY":
        cash = context.portfolio.total_value  # 总资产
        if context.portfolio.available_cash > 5000:  # 至少有5000可用现金
            order_target_value(security, cash)  # 全仓买入
            log.info("买入ETF [%s]" % security)

# 调仓买入：9:32执行，用于CHANGE信号
# 为什么延迟到9:32？因为9:30先卖出旧标的，需要等卖出成交后再买入
# 用90%资金买入（留10%缓冲，防止因滑点导致资金不足）
def my_sell2buy(context):
    if g.timing_signal == "CHANGE":
        security = g.check_out_list[0]
        cash = context.portfolio.total_value * 0.9  # 用90%资金，留缓冲
        if context.portfolio.available_cash > 5000:
            order_target_value(security, cash)
            log.info("买入ETF [%s]" % security)

# ==================== 工具函数 ====================

# 动量排名函数
# 对股票池中所有ETF计算动量得分，按得分降序排列
#
# 动量计算方法：乖离动量（Bias Momentum）
#   1. bias = 收盘价 / MA90（乖离率，衡量价格偏离均线的程度）
#   2. 对最近20天的乖离率做线性回归 → 斜率 × 10000 = 动量得分
#   3. 得分越高 → 乖离率上升越快 → 趋势越强
#
# 换仓加分机制：
#   如果某ETF是当前持仓（g.hold_stock），得分 × SwitchFactor（1.04）
#   目的：减少频繁换仓，只有新标的明显优于当前持仓时才换
#
# 返回值：[stock, score, adr] 的列表，按score降序排列
#   - stock: ETF代码
#   - score: 动量得分（换仓加分后）
#   - adr: 当日涨跌幅（%）
def get_rank(context, stock_pool):
    rank = []
    for stock in stock_pool:
        # 获取足够长的历史数据：90日均线需要90天 + 动量窗口20天
        data = attribute_history(stock, g.biasN + g.momentum_day, '1d', ['close'])
        # 乖离因子 = 收盘价 / 90日均线，取最近momentum_day天
        bias = (data.close / data.close.rolling(g.biasN).mean())[-g.momentum_day:]
        # 线性拟合：斜率 × 10000 作为动量得分（放大便于比较）
        score = np.polyfit(np.arange(g.momentum_day), bias/bias[0], 1)[0].real * 10000
        # 当日涨跌幅（%）
        adr = 100 * (data.close[-1] - data.close[-2]) / data.close[-2]
        # 换仓加分：当前持仓得分 × 1.04，降低换仓频率
        if stock == g.hold_stock:
            raise_x = g.SwitchFactor
        else:
            raise_x = 1
        rank.append([stock, score * raise_x, adr])
        # 更新动量历史序列（保留最近5天，用于一阶导数计算）
        g.stock_motion[stock].append(score)
        if len(g.stock_motion[stock]) > 5:
            g.stock_motion[stock].pop(0)
    # 打印排名日志
    str = ''
    for item in rank:
        str += "%s:%.2f:%.2f; " % (item[0], item[1], item[2])
    # 按动量得分降序排列（得分最高的排第一）：以 rank[1]倒序排序，得到排序后的rank
    rank.sort(key=lambda x: x[1], reverse=True)
    return rank

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

# Z-score 标准化函数
# 将最新值相对于历史序列做标准化：z = (最新值 - 均值) / 标准差
# 用途：将RSRS斜率转化为标准分，便于设定统一阈值
#   - z > 0：当前斜率高于历史平均 → 支撑强
#   - z < 0：当前斜率低于历史平均 → 阻力强
def get_zscore(slope_series):
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std

# Z-score序列的斜率函数
# 对最近K天的Z-score值做线性回归，返回斜率
# 用途：判断RSRS标准分的趋势方向
#   - 斜率 > 0：Z-score在上升 → 支撑力在增强 → 看多
#   - 斜率 < 0：Z-score在下降 → 支撑力在减弱 → 看空
def get_zscore_slope(z_scores):
    y = z_scores
    x = np.arange(len(z_scores))
    slope, intercept = np.polyfit(x, y, 1)
    return slope


# RSRS择时信号函数
# 基于阻力支撑相对强度（Resistance Support Relative Strength）判断大盘趋势
#
# RSRS核心原理：
#   - 对每日的(low, high)做线性回归：high = slope * low + intercept
#   - slope > 1：高点比低点涨得多 → 支撑力强 → 看多
#   - slope < 1：高点比低点涨得少 → 阻力强 → 看空
#   - 用Z-score标准化slope，再乘以r²（拟合度），得到rsrs_score
#
# 信号判断优先级（从高到低）：
#   1. 威廉指标WR超卖（>=97）→ 买入（抄底信号）
#   2. Z-score斜率下降 且 rsrs_score > 0 → 卖出（趋势反转预警）
#   3. 大盘下跌 + Z-score上升但不够强 → 卖出（弱势反弹不可信）
#   4. 大盘强势 + Z-score上升 → 买入（顺势做多）
#   5. rsrs_score > 阈值 → 买入
#   6. 其他情况 → 卖出
def get_timing_signal(context, stock):
    # --- Step 1: 计算当前RSRS指标 ---
    data = attribute_history(g.ref_stock, g.N, '1d', ['high', 'low', 'close'])
    # 对最近N天的(low, high)做线性回归，得到slope和r²
    intercept, slope, r2 = get_ols(data.low, data.high)
    g.slope_series.append(slope)
    # rsrs_score = Z-score × r²（用拟合度加权，线性关系越强越可信）
    rsrs_score = get_zscore(g.slope_series[-g.M:]) * r2
    g.rsrs_score_history.append(rsrs_score)
    # rsrs_slope = Z-score序列的趋势斜率（判断RSRS本身的趋势方向）
    rsrs_slope = get_zscore_slope(g.rsrs_score_history[-g.K:])

    # --- Step 2: 计算大盘指数收盘价趋势 ---
    # 对最近8天收盘价做线性回归，斜率反映短期趋势
    idex_slope = np.polyfit(np.arange(8), data.close[-8:], 1)[0].real
    # 维护slope序列长度（滑动窗口，只保留最近M+K天）
    g.slope_series.pop(0)
    g.rsrs_score_history.pop(0)

    log.info('rsrs_slope {:.3f}'.format(rsrs_slope) + ' rsrs_score {:.3f} '.format(rsrs_score)
    + ' idex_slope {:.3f} '.format(idex_slope))

    # --- Step 3: 威廉指标（WR）超卖信号 ---
    # WR指标：0~100，>=97表示极度超卖，是抄底信号
    # WR2=21日WR，WR1=14日WR，两者同时超卖时优先买入
    WR2, WR1 = WR([g.ref_stock], check_date=context.previous_date, N=21, N1=14, unit='1d', include_now=True)
    if WR1[g.ref_stock] >= 97 and WR2[g.ref_stock] >= 97:
        return "BUY"

    # --- Step 4: RSRS信号判断 ---
    # Z-score斜率下降（rsrs_slope < 0）但rsrs_score仍为正 → 上涨趋势即将结束
    if (rsrs_slope < 0 and rsrs_score > 0):
        return "SELL"
    # 大盘下跌趋势中（idex_slope < 0），即使Z-score上升但不够强 → 卖出
    if (idex_slope < 0) and (rsrs_slope > 0) and (rsrs_score < g.score_fall_thr):
        return "SELL"
    # 大盘强势上涨（idex_slope > 阈值）且Z-score上升 → 大胆买入
    if (idex_slope > g.idex_slope_raise_thr) and (rsrs_slope > 0):
        return "BUY"
    # rsrs_score超过买入阈值 → 买入
    if (rsrs_score > g.score_thr):
        return "BUY"
    # 其他情况：卖出
    else:
        return "SELL"



# 打印交易信息（调试用）
# 输出当天的成交记录和账户信息，便于回测时跟踪策略执行情况
def print_trade_info(context):
    # 打印当天成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：' + str(_trade))
    # 打印账户信息
    log.info('———————————————————————————————————————分割线1————————————————————————————————————————')