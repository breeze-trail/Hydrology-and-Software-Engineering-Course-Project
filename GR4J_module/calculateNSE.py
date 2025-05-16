import numpy as np

def getNSE(Qobs_mm, Q, days, **kwargs):
    # 精度评估
    # 1. 通过调整模型参数，使得模型得到更好的拟合效果的加分，具体视Nash-Sutcliffe指数
    # 2. 假设第一年365天作为预热期，消除产流水库和汇流水库初始值选取对模拟精度的影响
    count = 0                    # 计数器：记录总天数
    Q_accum = 0.0                # 记录累计径流量
    Q_ave = 0.0                  # 记录平均径流量
    NSE = 0.0                    # 记录纳什效率系数
    Q_diff1 = 0.0
    Q_diff2 = 0.0

    for i in range(365, days):
        count += 1
        Q_accum += Qobs_mm[i]

    Q_ave = Q_accum / count              # 计算观测流量平均值

    for i in range(365, days):
        Q_diff1 += (Qobs_mm[i] - Q[i])**2      # 计算Nash-Sutcliffe指数分子
        Q_diff2 += (Qobs_mm[i] - Q_ave)**2     # 计算Nash-Sutcliffe指数分母

    NSE = 1 - Q_diff1 / Q_diff2

    return NSE

    # 评估径流模拟效果：模型流域出口断面流量及模拟得到的流域出口断面流量