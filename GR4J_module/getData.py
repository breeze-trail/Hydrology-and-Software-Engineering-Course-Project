import numpy as np

def getData(path):
    para_path=path + '/GR4J_Parameter.txt'  # para_path: GR4J模型参数文件路径
    other_para_path=path + '/others.txt'    # other_para_path: 其他参数文件路径
    input_data_path=path + '/inputData.txt' # input_data_path: 输入数据文件路径

    # 加载GR4J模型参数
    para = np.loadtxt(para_path)
    params = {
        'x1': para[0],  # 产流水库容量 (mm)
        'x2': para[1],  # 地下水交换系数 (mm)
        'x3': para[2],  # 汇流水库容量 (mm)
        'x4': para[3]   # 单位线汇流时间 (天)
    }
    
    # 加载其他参数
    other_para = np.loadtxt(other_para_path)
    params.update({
        'area': other_para[0],           # 流域面积(km²)
        'upperTankRatio': other_para[1],  # 产流水库初始填充率 S0/x1
        'lowerTankRatio': other_para[2]   # 汇流水库初始填充率 R0/x3
    })
    
    # 加载输入数据
    data = np.loadtxt(input_data_path)
    params.update({
        'P': data[:, 0],     # 日降雨量(mm)
        'E': data[:, 1],     # 日蒸散发量(mm)
        'Qobs': data[:, 2],  # 观测流量(m³/s)
        'days': data.shape[0] # 数据总天数
    })
    
    # 流量单位转换 (m³/s -> mm/d)
    params['Qobs_mm'] = params['Qobs'] * 86.4 / params['area']
    
    return params

    """
    返回:
        dict: 包含所有必要数据的字典，键包括:
            - 'x1', 'x2', 'x3', 'x4': GR4J模型参数
            - 'area': 流域面积(km²)
            - 'upperTankRatio': 产流水库初始填充率
            - 'lowerTankRatio': 汇流水库初始填充率
            - 'P': 日降雨量(mm)
            - 'E': 日蒸散发量(mm)
            - 'Qobs': 观测流量(m³/s)
            - 'Qobs_mm': 转换后的观测流量(mm/d)
            - 'days': 数据总天数
    """