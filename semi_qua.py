# 基本框架 半定量评分系统
def calculate_absolute_weights(application=None):
    """计算基于文献分析(代码以及人工结合)的绝对权重值"""
    weights = {
        # 物理特性 (35%)
        'particle_size': 0.200,
        'pdi': 0.075,
        'zeta_potential': 0.075,
        
        # 载体特性 (26%)
        'carrier_type': 0.130,
        'surface_modification': 0.130,
        
        # 生物特性 (25%)
        'toxicity': 0.125,
        'stability': 0.125,
        
        # 递送特性 (10%)
        'cellular_uptake': 0.050,
        'biodistribution': 0.050,
        
        # 药物特性 (4%)
        'encapsulation_efficiency': 0.040
    }
    
    # 验证权重总和
    total_weight = sum(weights.values())
    if not 0.99 <= total_weight <= 1.01:  # 允许0.01的误差
        raise ValueError(f"Weight sum should be 1.0, got {total_weight}")
    
    if application:
        # 根据应用调整权重
        pass
    return weights

def validate_parameters(particle_size, pdi, zeta_potential):
    """验证输入参数的有效性"""
    # 类型检查
    if particle_size is not None and not isinstance(particle_size, (int, float)):
        raise TypeError("Particle size must be a number")
    if pdi is not None and not isinstance(pdi, (int, float)):
        raise TypeError("PDI must be a number")
    if zeta_potential is not None and not isinstance(zeta_potential, (int, float)):
        raise TypeError("Zeta potential must be a number")
    
    # 范围检查
    if particle_size is not None and (particle_size < 0 or particle_size > 1000):
        raise ValueError("Particle size should be between 0 and 1000 nm")
    if zeta_potential is not None and (zeta_potential < -100 or zeta_potential > 100):
        raise ValueError("Zeta potential should be between -100 and 100 mV")

def calculate_score(particle_size, pdi, zeta_potential, carrier_type, surface_modification, 
                   toxicity=None, stability=None, cellular_uptake=None, biodistribution=None,
                   encapsulation_efficiency=None, fpf=None, mmad=None, application=None):
    """
    计算TCM纳米载体的综合评分，评估其肺部递送潜力
    
    参数:
    particle_size (float): 纳米载体粒径(nm)
    pdi (float): 多分散指数(0-1)
    zeta_potential (float): Zeta电位(mV)
    carrier_type (str): 载体类型，如'SLN', 'NLC', 'PLGA', 'Liposome'等
    surface_modification (str): 表面修饰类型，如'None', 'PEG', 'Chitosan'等
    toxicity (float, optional): 毒性评分，如细胞存活率百分比
    stability (float, optional): 稳定性评分，如储存一周后的物理稳定性百分比
    cellular_uptake (float, optional): 细胞摄取率百分比
    biodistribution (float, optional): 肺部分布百分比或比率
    encapsulation_efficiency (float, optional): 包封率百分比
    fpf (float, optional): 粒径分布函数(FPF)
    mmad (float, optional): 中位粒径(MMAD)
    application (str, optional): 应用类型
    
    返回:
    float: 综合评分(0-5分)
    """
    # 验证参数
    validate_parameters(particle_size, pdi, zeta_potential)
    
    # 粒径评分函数
    def size_score(size):
        if size is None: return 3
        if size < 50: return 5
        elif 50 <= size < 100: return 4
        elif 100 <= size < 200: return 3
        elif 200 <= size < 300: return 0
        else: return 0
    
    # PDI评分函数
    def pdi_score(value):
        if value is None: return 3
        if value > 1:
            normalized_value = value / 100 if value > 10 else value / 10
            value = min(normalized_value, 1)
        
        if value < 0.1: return 5
        elif value < 0.2: return 4
        elif value < 0.3: return 3
        elif value < 0.4: return 2
        elif value < 1.0: return 1
        else: return 0
    
    # Zeta电位评分函数
    def zeta_score(value):
        if value is None: return 0
        
        abs_zeta = abs(value)
        if abs_zeta > 30: return 5
        elif abs_zeta > 20: return 4
        elif abs_zeta > 10: return 2
        else: return 0
    
    # 载体类型评分函数
    def carrier_score(type_str):
        if type_str is None: 
            return 3
        scores = {
            'NLC': 5,      # 纳米结构脂质载体
            'SLN': 4,      # 固体脂质纳米粒
            'PLGA': 4,     # PLGA聚合物纳米粒
            'Liposome': 3, # 脂质体
            'Chitosan': 4, # 壳聚糖纳米粒
            'Inorganic': 2 # 无机纳米粒
        }
        return scores.get(type_str, 3)  # 未知类型返回默认值3
    
    # 表面修饰评分函数
    def surface_score(mod_str):
        if mod_str is None:
            return 3
        scores = {
            'PEG': 5,        # PEG修饰
            'Chitosan': 4,   # 壳聚糖修饰
            'Cationic': 3,   # 阳离子修饰
            'Antibody': 3,   # 抗体修饰
            'None': 1,       # 无修饰
            'Poloxamer 188': 4  # 新的表面修饰类型 特定修饰
        }
        return scores.get(mod_str, 3)  # 未知类型返回默认值3
    
    # 毒性评分函数
    def toxicity_score(viability=None):
        if viability is None: return 3
        if viability >= 90: return 5
        elif viability >= 80: return 4
        elif viability >= 70: return 3
        elif viability >= 60: return 2
        else: return 1
    
    # 稳定性评分函数
    def stability_score(stab=None):
        if stab is None: return 3
        if stab >= 90: return 5
        elif stab >= 80: return 4
        elif stab >= 70: return 3
        else: return 2
    
    # 细胞摄取评分函数
    def uptake_score(rate=None):
        if rate is None: return 3
        if rate >= 80: return 5
        elif rate >= 60: return 4
        elif rate >= 40: return 3
        elif rate >= 20: return 2
        else: return 1
    
    # 生物分布评分函数
    def distribution_score(lung_dist=None):
        if lung_dist is None: return 3
        if lung_dist >= 60: return 5
        elif lung_dist >= 40: return 4
        elif lung_dist >= 20: return 3
        elif lung_dist >= 10: return 2
        else: return 1
    
    # 包封率评分函数
    def ee_score(ee=None):
        if ee is None: return 3
        if ee >= 90: return 5
        elif ee >= 80: return 4
        elif ee >= 70: return 3
        elif ee >= 60: return 2
        else: return 1

    # FPF评分函数
    def fpf_score(value=None):
        if value is None: return 3
        if value >= 70: return 5
        elif value >= 60: return 4
        elif value >= 50: return 3
        elif value >= 40: return 2
        else: return 1

    # MMAD评分函数
    def mmad_score(value=None):
        if value is None: return 3
        if 1 <= value <= 5: return 5
        elif value < 1: return 2
        else: return 1
    
    # 使用新的权重分配
    weights = calculate_absolute_weights(application)
    
    # 计算基础评分
    scores = {
        'particle_size': size_score(particle_size) * weights['particle_size'],
        'pdi': pdi_score(pdi) * weights['pdi'],
        'zeta_potential': zeta_score(zeta_potential) * weights['zeta_potential'],
        'carrier_type': carrier_score(carrier_type) * weights['carrier_type'],
        'surface_modification': surface_score(surface_modification) * weights['surface_modification']
    }
    
    # 添加可选参数评分
    if toxicity is not None:
        scores['toxicity'] = toxicity_score(toxicity) * weights['toxicity']
    if stability is not None:
        scores['stability'] = stability_score(stability) * weights['stability']
    if cellular_uptake is not None:
        scores['cellular_uptake'] = uptake_score(cellular_uptake) * weights['cellular_uptake']
    if biodistribution is not None:
        scores['biodistribution'] = distribution_score(biodistribution) * weights['biodistribution']
    if encapsulation_efficiency is not None:
        scores['encapsulation_efficiency'] = ee_score(encapsulation_efficiency) * weights['encapsulation_efficiency']
    
    # 计算总分并归一化
    total_weight = sum(weights[param] for param in scores.keys())
    raw_score = sum(scores.values()) / total_weight
    
    # 确保分数在0-5范围内
    normalized_score = max(0, min(5, raw_score))
    
    return round(normalized_score, 2)

# 评分解释函数
def interpret_score(score):
    """解释评分含义"""
    if score >= 4:
        return "高肺部递送潜力，建议优先考虑"
    elif score >= 2.5:
        return "中等肺部递送潜力，需进一步优化"
    else:
        return "低肺部递送潜力，不推荐用于肺部递送"
