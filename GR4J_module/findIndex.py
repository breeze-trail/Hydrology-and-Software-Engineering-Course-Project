import numpy as np
import matplotlib.pyplot as plt
from drawFlow import *
from GR4J import *
from calculateNSE import *
from getData import *
import time as t


if __name__ == "__main__":
    clock = t.time()
    # 获取数据
    data = getData("data")
    ls1 = []
    ls2 = []
    with open("result.txt","r") as res:
        ls1 = res.readlines()
    for i in range(len(ls1)):
        ls1[i] = ls1[i].split(' ')
        for j in range(4):
            ls1[i][j] = float(ls1[i][j])
        ls1[i][4] = float(ls1[i][4][:-1])
    ls1.sort(key=lambda a:-a[4])
    with open("result2.txt","r") as res:
        ls2 = res.readlines()
    n = len(ls2)
    with open("index.txt","w") as get:
        get.write(f"{n//5324-1}\n{(n//484-1)%11}\n{(n//44-1)%11}\n{(n//4-1)%11}\n{(n-1)%4}")
    # exit(0)
# for i in np.arange(100.00,1200.00,100.00):
#     for j in np.arange(-5.00,3.00,1.00):
#         for k in np.arange(20.00,300.00,10.00):
#             for l in np.arange(0.10,7.00,0.30):

    # 打印参数和NSE
    # print("-------------------最优参数和NSE---------------------")
    # print("x1: " + str(data["x1"]) + "\n" + 
    #       "x2: " + str(data["x2"]) + "\n" + 
    #       "x3: " + str(data["x3"]) + "\n" + 
    #       "x4: " + str(data["x4"]) + "\n" + 
    #       "NSE: " + str(data["NSE"]))
    # print("----------------------------------------------------")
