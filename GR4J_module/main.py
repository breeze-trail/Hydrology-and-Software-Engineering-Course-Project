import numpy as np
import matplotlib.pyplot as plt
from drawFlow import *
from GR4J import *
from calculateNSE import *
from getData import *
import time

#100.00 3.00 60.00 1.10 0.8300945391
if __name__ == "__main__":
    # 获取数据
      data = getData("data")

      start = time.time()
      cnt = 0
      all = 100 * 20 * 10 * 20
      with open("..\\result3.txt","w") as res:
            for i in np.arange(100.0 - 10.0,100.0 + 10, 0.2):
                  for j in np.arange(3.00 - 1.00, 3.00 + 1.00, 0.1):
                        for k in np.arange(60.0 - 5 ,60.0 + 5, 0.1):
                              for l in np.arange(1.10 - 0.5, 1.10 + 0.5, 0.05):
                                    data["x1"] = i
                                    data["x2"] = j
                                    data["x3"] = k
                                    data["x4"] = l
                                    data["Q"] = GR4J(**data)
                                    data["NSE"] = getNSE(**data)
                                    
                                    cnt+=1
                                    
                                    print(data["NSE"])
                                    print(str(time.time() - start) + "s")
                                    print(str(cnt) + '/' + str(all) + '\n')
                                    
                                    res.write("{:.2f} {:.2f} {:.2f} {:.2f} {:.8f}\n".format(i,j,k,l,data["NSE"]))
                                    

    #打印参数和NSE
      print("-------------------最优参数和NSE---------------------")
      print("x1: " + str(data["x1"]) + "\n" + 
          "x2: " + str(data["x2"]) + "\n" + 
          "x3: " + str(data["x3"]) + "\n" + 
          "x4: " + str(data["x4"]) + "\n" + 
          "NSE: " + str(data["NSE"]))
      print("----------------------------------------------------")