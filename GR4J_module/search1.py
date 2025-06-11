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
    with open("result.txt","w") as res:
        for i in np.arange(100.00,1200.00,100.00):
            for j in np.arange(-5.00,3.00,1.00):
                for k in np.arange(20.00,300.00,10.00):
                    for l in np.arange(0.10,7.00,0.30):
                            
                        data["x1"] = i
                        data["x2"] = j
                        data["x3"] = k
                        data["x4"] = l

                        # GR4J模型计算
                        data["Q"] = GR4J(**data)

                        #NSE精度评估
                        getans = getNSE(**data)
                        res.write("{:.2f} {:.2f} {:.2f} {:.2f} {:.8f}\n".format(i,j,k,l,getans))
                print(t.time() - clock)
    

    # 打印参数和NSE
    # print("-------------------最优参数和NSE---------------------")
    # print("x1: " + str(data["x1"]) + "\n" + 
    #       "x2: " + str(data["x2"]) + "\n" + 
    #       "x3: " + str(data["x3"]) + "\n" + 
    #       "x4: " + str(data["x4"]) + "\n" + 
    #       "NSE: " + str(data["NSE"]))
    # print("----------------------------------------------------")
