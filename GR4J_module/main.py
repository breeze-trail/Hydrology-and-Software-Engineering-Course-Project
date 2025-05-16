import numpy as np
import matplotlib.pyplot as plt
from drawFlow import *
from GR4J import *
from calculateNSE import *
from getData import *


if __name__ == "__main__":
    # 获取数据
    data = getData("data")

    # GR4J模型计算
    Q = GR4J(**data)

    #NSE精度评估
    NSE = getNSE(**data)
    
    # 绘制径流与预测径流图像
    draw(**data)