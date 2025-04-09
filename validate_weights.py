# 用于验证半定量评分系统,利用原文数据验证相关性,涉及spearman相关性分析. 调用了semi_qua.py中的calculate_score函数
# 输入文件可以是Markdown或CSV格式,列名像nanocarriers.csv
import pandas as pd
import numpy as np
import sys
import argparse
import os
import re
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from semi_qua import calculate_score

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="验证半定量评分系统权重")
    parser.add_argument('-i', '--input', required=True, help="输入文件路径(Markdown或CSV)")
    parser.add_argument('-o', '--output', help="输出目录")
    return parser.parse_args()

def load_from_markdown(file_path):
    """从Markdown文件加载数据"""
    print(f"正在从Markdown文件加载数据: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 跳过前两行(标题和分隔符)
    data_lines = [line for line in lines[2:] if line.strip()]
    
    formulations = []
    for line in data_lines:
        parts = line.strip().split('|')
        if len(parts) > 10:  
            particle_size = parts[2].strip()
            if '-' in particle_size:
                low, high = map(float, particle_size.split('-'))
                particle_size = (low + high) / 2
            elif particle_size and particle_size.lower() != 'na':
                particle_size = float(particle_size)
            else:
                particle_size = None
            
            # 创建制剂字典
            form = {
                'name': parts[1].strip(),
                'particle_size': particle_size,
                'pdi': float(parts[4].strip()) if parts[4].strip() and parts[4].strip().lower() != 'na' else None,
                'zeta_potential': float(parts[6].strip()) if parts[6].strip() and parts[6].strip().lower() != 'na' else None,
                'carrier_type': parts[8].strip() if parts[8].strip().lower() != 'na' else None,
                'surface_modification': parts[9].strip() if parts[9].strip().lower() != 'na' else None,
                'FPF': float(parts[10].strip()) if parts[10].strip() and parts[10].strip().lower() != 'na' else None,
                'MMAD': float(parts[12].strip()) if parts[12].strip() and parts[12].strip().lower() != 'na' else None
            }
            formulations.append(form)
    
    return formulations

def load_from_csv(file_path):
    """从CSV文件加载数据"""
    print(f"正在从CSV文件加载数据: {file_path}")
    df = pd.read_csv(file_path)
    
    formulations = []
    for _, row in df.iterrows():
        form = {
            'name': row.get('name', ''),
            'particle_size': row.get('particle_size') if pd.notna(row.get('particle_size')) else None,
            'pdi': row.get('pdi') if pd.notna(row.get('pdi')) else None,
            'zeta_potential': row.get('zeta') if pd.notna(row.get('zeta')) else None,
            'carrier_type': row.get('carrier_type') if pd.notna(row.get('carrier_type')) else None,
            'surface_modification': row.get('surface_modify') if pd.notna(row.get('surface_modify')) else None,
            'FPF': row.get('FPF') if pd.notna(row.get('FPF')) else None,
            'MMAD': row.get('mmad') if pd.notna(row.get('mmad')) else None
        }
        formulations.append(form)
    
    return formulations

def load_data(file_path=None):
    """根据文件类型加载数据"""
    if file_path:
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.csv':
            return load_from_csv(file_path)
        elif ext.lower() == '.md':
            return load_from_markdown(file_path)
        else:
            print(f"不支持的文件类型: {ext}")
            return get_default_formulations()
    else:
        return get_default_formulations()

def get_default_formulations():
    """返回默认的制剂数据"""
    # 将文本性能描述转换为数值
    performance_mapping = {
        'high': 5.0,
        'medium-high': 4.0,
        'medium': 3.0,
        'medium-low': 2.0,
        'low': 1.0
    }

    # 默认的纳米制剂数据 5个自主添加 可删可修改 不影响验证
    return [
        {
            'name': 'cur-lip-lc',
            'particle_size': 94.65,
            'pdi': 0.26,
            'zeta_potential': None,  # NA值转为None
            'carrier_type': 'Liposome',
            'surface_modification': None,  # NA值转为None
            'FPF': 46.71,
            'MMAD': 5.81
        },
        {
            'name': 'salbutamol-lip-asth',
            'particle_size': 165,  
            'pdi': 1.12,
            'zeta_potential': 9.74,
            'carrier_type': 'Liposome',
            'surface_modification': 'None',
            'FPF': 64.01,
            'MMAD': 3.49
        },
        {
            'name': 'ma-nlc-copd',
            'particle_size': 19.67,
            'pdi': 0.21,
            'zeta_potential': -5.18,
            'carrier_type': 'NLC',
            'surface_modification': 'None',
            'FPF': 68.90,
            'MMAD': 3.36
        },
        {
            'name': 'nint-plga-LF',
            'particle_size': 179,
            'pdi': 0.19,
            'zeta_potential': -23.4,
            'carrier_type': 'PLGA',
            'surface_modification': 'None',
            'FPF': 64.9,
            'MMAD': 4.20
        },
        {
            'name': 'COX2inhibi-PLGA-Lc',
            'particle_size': 230.4,
            'pdi': 0.075,
            'zeta_potential': 18.7,
            'carrier_type': 'PLGA',
            'surface_modification': 'Poloxamer 188',
            'FPF': 71,
            'MMAD': 5.65
        }
    ]

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 加载数据
    formulations = load_data(args.input)
    
    # 确保数据格式正确
    for form in formulations:
        # 处理字符串'NA'为None
        for key in form.keys():
            if form[key] == 'NA':
                form[key] = None
        
        # 确保载体类型格式正确
        if form.get('carrier_type') and isinstance(form['carrier_type'], str):
            if form['carrier_type'].lower() == 'liposome':
                form['carrier_type'] = 'Liposome'
            elif form['carrier_type'].lower() == 'plga':
                form['carrier_type'] = 'PLGA'
            elif form['carrier_type'].lower() == 'nlc':
                form['carrier_type'] = 'NLC'
            elif form['carrier_type'].lower() == 'sln':
                form['carrier_type'] = 'SLN'
            elif form['carrier_type'].lower() == 'polymer':
                form['carrier_type'] = 'PLGA'  # 假设polymer是PLGA类型
    
    # 计算每个制剂的评分
    for formulation in formulations:
        score = calculate_score(
            particle_size=formulation.get('particle_size'),
            pdi=formulation.get('pdi'),
            zeta_potential=formulation.get('zeta_potential'),
            carrier_type=formulation.get('carrier_type'),
            surface_modification=formulation.get('surface_modification'),
            encapsulation_efficiency=formulation.get('encapsulation_efficiency'),
            stability=formulation.get('stability'),
            cellular_uptake=formulation.get('cellular_uptake'),
            biodistribution=formulation.get('biodistribution')
        )
        formulation['score'] = score
        print(f"{formulation['name']}: {score:.2f}")
    
    # 使用FPF作为性能指标计算Spearman相关系数
    fpf_values = []
    score_values = []
    
    for form in formulations:
        if 'FPF' in form and form['FPF'] is not None:
            fpf_values.append(form['FPF'])
            score_values.append(form['score'])
    
    # 获取MMAD值和对应的评分值
    mmad_values = []
    mmad_score_values = []
    for form in formulations:
        if 'MMAD' in form and form['MMAD'] is not None:
            mmad_values.append(form['MMAD'])
            mmad_score_values.append(form['score'])
    
    # 计算FPF与评分的相关性
    if len(fpf_values) >= 3:  # 至少需要3个值才能计算相关系数
        correlation_fpf, p_value_fpf = spearmanr(score_values, fpf_values)
        print(f"FPF相关性: Spearman's ρ = {correlation_fpf:.2f}, p-value = {p_value_fpf:.4f}")
    else:
        print("FPF数据不足，无法计算相关性")
    
    # 计算MMAD与评分的相关性 - 使用原始MMAD值
    if len(mmad_values) >= 3:
        correlation_mmad, p_value_mmad = spearmanr(mmad_score_values, mmad_values)
        print(f"MMAD相关性: Spearman's ρ = {correlation_mmad:.2f}, p-value = {p_value_mmad:.4f}")
    else:
        print("MMAD数据不足，无法计算相关性")
    
    # 设置输出路径
    output_dir = args.output if args.output else '.'
    os.makedirs(output_dir, exist_ok=True)
    
    # 可视化FPF评分与性能的关系
    if len(fpf_values) >= 2:
        plt.figure(figsize=(10, 6))
        plt.scatter(score_values, fpf_values)
        for i, form in enumerate([f for f in formulations if 'FPF' in f and f['FPF'] is not None]):
            plt.annotate(form['name'], (form['score'], form['FPF']))
        plt.xlabel('Calculated Score')
        plt.ylabel('FPF (%)')
        plt.title('Correlation between Scoring System and Fine Particle Fraction')
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, 'fpf_correlation.png'))
        plt.show()
    
    # 可视化MMAD评分与性能的关系
    if len(mmad_values) >= 2:
        plt.figure(figsize=(10, 6))
        plt.scatter(mmad_score_values, mmad_values)
        
        # 添加理想范围标注（1-5 μm）
        plt.axhspan(1, 5, alpha=0.2, color='green', label='Ideal MMAD Range (1-5 μm)')
        
        # 每个点添加标签
        for i, form in enumerate([f for f in formulations if 'MMAD' in f and f['MMAD'] is not None]):
            plt.annotate(form['name'], (form['score'], form['MMAD']))
        
        plt.xlabel('Calculated Score')
        plt.ylabel('MMAD (μm)')
        plt.title('Correlation between Scoring System and MMAD')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, 'mmad_correlation.png'))
        plt.close()  
    
    # 如果两个图都创建了，显示完成信息
    if len(fpf_values) >= 2 and len(mmad_values) >= 2:
        print(f"分析完成。图表已保存至 {output_dir} 目录")

if __name__ == "__main__":
    main()
