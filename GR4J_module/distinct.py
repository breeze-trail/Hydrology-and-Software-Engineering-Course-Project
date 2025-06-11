import numpy as np
import matplotlib.pyplot as plt
from drawFlow import *
from GR4J import *
from calculateNSE import *
from getData import *
import time as t


if __name__ == "__main__":
    # 获取数据
    data = getData("data")
    ls = []
    with open("result3.txt","r") as res:
        ls = res.readlines()
    ls = list(set(ls))
    with open("result3.txt","w") as res:
        res.writelines(ls)
    

    # 打印参数和NSE
    # print("-------------------最优参数和NSE---------------------")
    # print("x1: " + str(data["x1"]) + "\n" + 
    #       "x2: " + str(data["x2"]) + "\n" + 
    #       "x3: " + str(data["x3"]) + "\n" + 
    #       "x4: " + str(data["x4"]) + "\n" + 
    #       "NSE: " + str(data["NSE"]))
    # print("----------------------------------------------------")
