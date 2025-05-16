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
    data["Q"] = GR4J(**data)

    #NSE精度评估
    data["NSE"] = getNSE(**data)

    #打印参数和NSE
    print("-------------------最优参数和NSE---------------------")
    print("x1: " + str(data["x1"]) + "\n" + 
          "x2: " + str(data["x2"]) + "\n" + 
          "x3: " + str(data["x3"]) + "\n" + 
          "x4: " + str(data["x4"]) + "\n" + 
          "NSE: " + str(data["NSE"]))
    print("----------------------------------------------------")
    # 绘制径流与预测径流图像
    draw(**data)
