import numpy as np
from curveCalculate import *

def GR4J(x1, x2, x3, x4, upperTankRatio, lowerTankRatio, P, E, days):

    # 初始化变化，存储GR4J模型中间变量值 
    Pn = np.zeros(days)   # Pn：降雨扣除损失（蒸发）后得净雨
    En = np.zeros(days)   # En：当日蒸发未被满足部分
    Ps = np.zeros(days)   # Ps：中间变量，记录净雨补充土壤含水量
    Es = np.zeros(days)   # Es: 中间变量，记录剩余蒸发能力消耗土壤含水量
    Perc = np.zeros(days) # Perc: 中间变量，记录产流水库壤中流产流量
    Pr = np.zeros(days)   # Pr: 记录产流总量

    # 根据输入参数x4计算S曲线以及单位线，这里假设单位线长度UH1为10，UH2为20;即x4取值不应该大于10
    maxDayDelay = 10
    # 定义几个数组以存储SH1,UH1,SH2,UH2
    SH1 = np.zeros(maxDayDelay)
    UH1 = np.zeros(maxDayDelay)
    SH2 = np.zeros(2*maxDayDelay)
    UH2 = np.zeros(2*maxDayDelay)
    # 计算SH1以及SH2
    for i in range(maxDayDelay):
        SH1[i] = SH1_CURVE(i+1, x4)  # Python索引从0开始，天数从1开始

    for i in range(2*maxDayDelay):
        SH2[i] = SH2_CURVE(i+1, x4)

    # 计算UH1以及UH2
    for i in range(maxDayDelay):
        if i == 0:
            UH1[i] = SH1[i]
        else:
            UH1[i] = SH1[i] - SH1[i-1]

    for i in range(2*maxDayDelay):
        if i == 0:
            UH2[i] = SH2[i]
        else:
            UH2[i] = SH2[i] - SH2[i-1]

    # 计算逐日En及Pn值,En及Pn为GR4J模型得输入，可以提前计算出来
    for i in range(days):
        if P[i] >= E[i]:  # 若当日降雨量大于等于当日蒸发量，净降雨量Pn=P-E,净蒸发能力En=0
            Pn[i] = P[i] - E[i]
            En[i] = 0
        else:              # 若当日降雨量小于当日蒸发量，净效降雨量Pn=0,净蒸发能力En=E-P
            Pn[i] = 0
            En[i] = E[i] - P[i]

    # 定义一些产汇流计算需要用到得数值及数组
    S0 = upperTankRatio * x1            # 产流水库初始土壤含水量=比例*产流水库容量
    R0 = lowerTankRatio * x3            # 汇流水库初始土壤含水量=比例*汇流水库容量
    S = np.zeros(days)                 # S：产流水库逐日水量
    R = np.zeros(days)                 # R：汇流水库逐日水量
    UH_Fast = np.zeros((days, maxDayDelay))    # UH_Fast: 用于记录UH1单位线作用下得产流信息
    UH_Slow = np.zeros((days, 2*maxDayDelay))  # UH_Slow: 用于记录UH2单位线作用下得产流信息
    S_TEMP = S0                         # 用S_TEMP存储当前产流水库储量
    R_TEMP = R0                         # 用R_TEMP存储当前汇流水库储量
    Qr = np.zeros(days)                # Qr：汇流水库快速流出流量
    Qd = np.zeros(days)                # Qd：汇流水库慢速流出流量
    Q = np.zeros(days)                 # Q：汇流总出流量

    # 获取En及Pn值后，更新产流水库蓄水量
    for i in range(days):
        S[i] = S_TEMP
        R[i] = R_TEMP
        
        # Pn(i)及En(i)有且仅有一个大于0，所以下面两个if判断只可能一个为真
        if Pn[i] != 0:  # 净雨量大于0，此时一部分净雨形成地面径流，一部分下渗
            Ps[i] = x1 * (1 - ((S[i]/x1)**2)) * np.tanh(Pn[i]/x1) / (1 + S[i]/x1 * np.tanh(Pn[i]/x1))
            Es[i] = 0
        
        if En[i] != 0:  # 净蒸发能力大于0，此时土壤中水分一部分用于消耗
            Ps[i] = 0
            Es[i] = (S[i] * (2 - (S[i]/x1)) * np.tanh(En[i]/x1)) / (1 + (1 - S[i]/x1) * np.tanh(En[i]/x1))
        
        # 更新上层水库蓄水量
        S_TEMP = S[i] - Es[i] + Ps[i]
        Ratio_TEMP = S_TEMP / x1
        
        # 计算产流水库渗漏，这部分可以视作壤中流
        Perc[i] = S_TEMP * (1 - (1 + (4.0/9.0 * (S_TEMP/x1))**4)**(-0.25))
        
        # 计算产流总量,其中Pn-Ps可以视作为地表产流
        Pr[i] = Perc[i] + (Pn[i] - Ps[i])
        
        # 更新当前产流水库水量，作为次日产流水库水量
        S_TEMP = S_TEMP - Perc[i]
        
        # 至此产流过程全部结束，进入汇流阶段
        
        # 汇流计算
        # 计算地表水与地下水之间得水量交换
        F = x2 * (R[i]/x3)**3.5
        
        # 计算地表水汇流，将产流量按照90%(快速)和10%(慢速)划分
        # 快速地表径流汇流使用单位先UH1; 慢速地表径流汇流使用单位先UH2; 
        R_Fast = Pr[i] * 0.9
        R_Slow = Pr[i] * 0.1
        
        if i == 0:
            UH_Fast[i, :] = R_Fast * UH1  # 第1时段产流量在时间上的分配
            UH_Slow[i, :] = R_Slow * UH2  # 第1时段产流量在时间上的分配
        else:
            UH_Fast[i, :] = R_Fast * UH1  # 先计算当前时段产流量在时间上得分配
            for j in range(maxDayDelay-1):
                UH_Fast[i, j] = UH_Fast[i, j] + UH_Fast[i-1, j+1]  # 第2时段总汇流=第2时段产流量当前汇流+第1时段产流量第2部分汇流
            
            UH_Slow[i, :] = R_Slow * UH2  # 先计算当前时段产流量在时间上得分配
            for j in range(2*maxDayDelay-1):
                UH_Slow[i, j] = UH_Slow[i, j] + UH_Slow[i-1, j+1]  # 第2时段总汇流=第2时段产流量当前汇流+第1时段产流量第2部分汇流
        
        # 更新汇流水库水量变化
        R_TEMP = max(0, R_TEMP + UH_Fast[i, 0] + F)
        
        # 计算汇流水库快速流出流量
        Qr[i] = R_TEMP * (1 - (1 + (R_TEMP/x3)**4)**(-0.25))
        
        # 再次更新汇流水库水量变化
        R_TEMP = R_TEMP - Qr[i]
        
        # 计算汇流水库慢速流出流量
        Qd[i] = max(0, UH_Slow[i, 0] + F)
        
        # 计算汇流总出流量
        Q[i] = Qr[i] + Qd[i]       # Pr: 记录产流总量

        #输出汇流总出流量
        return Q