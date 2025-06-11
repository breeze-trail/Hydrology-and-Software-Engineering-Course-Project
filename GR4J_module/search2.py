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
    with open("result.txt","r") as res:
        ls = res.readlines()
    for i in range(len(ls)):
        ls[i] = ls[i].split(' ')
        for j in range(4):
            ls[i][j] = float(ls[i][j])
        ls[i][4] = float(ls[i][4][:-1])
    ls.sort(key=lambda a:-a[4])
    # exit(0)
# for i in np.arange(100.00,1200.00,100.00):
#     for j in np.arange(-5.00,3.00,1.00):
#         for k in np.arange(20.00,300.00,10.00):
#             for l in np.arange(0.10,7.00,0.30):
    tot = 10 * 11 * 11
    with open("result2.txt","r") as res:
        n = len(res.readlines())
        tot -= n // 44
        befround = n // 5324
        befi = n // 484 % 11
        befj = n // 44 % 11
        befk = n // 4 % 11
        befl = n % 4
    done = 0
    changeround = True
    changei = True
    changej = True
    changek = True
    clock = t.time()
    with open("result2.txt","a") as res:
        for round in range(befround,10):
            now = ls[round]
            starti = befi if changeround else 0.0
            for i in np.arange(now[0] + starti * 10.00, now[0] + 100.01, 10.00):
                startj = befj if changeround and changei else 0.0
                for j in np.arange(now[1] + startj * 0.10, now[1] + 1.01, 0.10):
                    startk = befk if changeround and changei and changej else 0.0
                    for k in np.arange(now[2] + startk * 1.00, now[2] + 10.01, 1.00):
                        startl = befl if changeround and changei and changej and changek else 0.0
                        for l in np.arange(now[3] + startl * 0.10, now[3] + 0.31, 0.10):
                                
                            data["x1"] = i
                            data["x2"] = j
                            data["x3"] = k
                            data["x4"] = l

                            # GR4J模型计算
                            data["Q"] = GR4J(**data)

                            #NSE精度评估
                            getans = getNSE(**data)
                        
                            res.write("{:.2f} {:.2f} {:.2f} {:.2f} {:.10f}\n".format(i,j,k,l,getans))
                        changek = False
                    changej = False
                    tot -= 1
                    done += 1
                    print(f"Rest: {tot}\nCur: {now}, {i}, {j}\nUsed Time: {t.time() - clock}s\n Est Time: {(t.time() - clock) / done * tot}s")
                changei = False
            changeround = False
    

    # 打印参数和NSE
    # print("-------------------最优参数和NSE---------------------")
    # print("x1: " + str(data["x1"]) + "\n" + 
    #       "x2: " + str(data["x2"]) + "\n" + 
    #       "x3: " + str(data["x3"]) + "\n" + 
    #       "x4: " + str(data["x4"]) + "\n" + 
    #       "NSE: " + str(data["NSE"]))
    # print("----------------------------------------------------")
