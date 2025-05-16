import matplotlib.pyplot as plt
import numpy as np

def draw(days, Q, Qobs_mm, NSE, **kwargs):
    plt.rcParams["font.family"] = ["SimHei"]
    plt.show()
    axis = np.arange(1, days+1)
    plt.figure(figsize=(12, 6))
    plt.plot(axis, Q, 'r--', label='模拟径流量',linewidth=1)
    plt.plot(axis, Qobs_mm, 'k-', label='观测径流量',linewidth=1)
    plt.title(f'GR4J模型模拟效果图, NSE={NSE:.4f}')
    plt.xlabel('时间（天）')
    plt.ylabel('流量（mm/d）')
    plt.legend()
    plt.grid(True)
    plt.show()