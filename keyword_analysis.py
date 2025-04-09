import csv
import re
from collections import Counter

# 定义要查找的关键参数列表
key_parameters = [
    'particle size', 'size', 'diameter',
    'zeta potential', 
    'PDI', 'polydispersity', 
    'carrier type', 'nanocarrier', 'carrier',
    'surface modification', 'surface charge', 'surface coating', 'PEG', 'chitosan', 'hyaluronic acid',
    'drug loading', 'loading efficiency', 'drug content',
    'encapsulation efficiency', 'entrapment',
    'release profile', 'sustained release', 'controlled release',
    'stability', 'storage stability',
    'toxicity', 'cytotoxicity', 'biocompatibility',
    'targeting ability', 'targeting efficiency', 'specific targeting',
    'cellular uptake', 'internalization', 'cell membrane penetration',
    'biodistribution', 'lung distribution', 'pulmonary distribution',
    'biodegradability', 'degradation',
    'inhalation efficiency', 'lung deposition', 'aerodynamic diameter',
    'mucus penetration', 'mucosal barrier'
]

# 分类参数
parameter_categories = {
    'physical properties': ['particle size', 'size', 'diameter', 'zeta potential', 'PDI', 'polydispersity'],
    'carrier properties': ['carrier type', 'nanocarrier', 'carrier', 'surface modification', 'surface charge', 'surface coating', 'PEG', 'chitosan', 'hyaluronic acid'],
    'drug properties': ['drug loading', 'loading efficiency', 'drug content', 'encapsulation efficiency', 'entrapment', 'release profile', 'sustained release', 'controlled release'],
    'biological properties': ['stability', 'storage stability', 'toxicity', 'cytotoxicity', 'biocompatibility', 'targeting ability', 'targeting efficiency', 'specific targeting'],
    'delivery properties': ['cellular uptake', 'internalization', 'cell membrane penetration', 'biodistribution', 'lung distribution', 'pulmonary distribution', 'biodegradability', 'degradation'],
    'pulmonary specific': ['inhalation efficiency', 'lung deposition', 'aerodynamic diameter', 'mucus penetration', 'mucosal barrier']
}

# 逆映射，从参数到类别
param_to_category = {}
for category, params in parameter_categories.items():
    for param in params:
        param_to_category[param] = category

# 初始化计数器
parameter_counts = Counter()
category_counts = Counter()
years = []

def process_file(file, reader):
    """处理CSV文件的函数"""
    for row in reader:
        abstract = row.get('Abstract', '').lower()
        title = row.get('Title', '').lower()
        keywords = row.get('Keywords', '').lower()
        year = row.get('Year', '')
        
        if year:
            try:
                years.append(int(year))
            except ValueError:
                pass
        
        # 合并文本搜索
        combined_text = f'{title} {abstract} {keywords}'
        
        # 统计关键参数出现次数
        for param in key_parameters:
            # 针对PDI特殊处理
            if param in ['PDI', 'polydispersity']:
                # 扩展搜索以捕获更多PDI相关表述
                patterns = [
                    r'\bPDI\b', 
                    r'\bpolydispersity\b', 
                    r'\bpolydispersity index\b',
                    r'\bPdI\b',
                    r'\bpolydisperse\b',
                    r'\bdispersity\b'
                ]
                count = sum(len(re.findall(pattern, combined_text)) for pattern in patterns)
            else:
                # 原有搜索方式
                count = len(re.findall(r'\b' + re.escape(param) + r'\b', combined_text))
            
            if count > 0:
                parameter_counts[param] += count
                category_counts[param_to_category.get(param, 'unknown')] += count

# 尝试不同编码读取CSV文件
try:
    # 读取CSV文件并进行分析 - 使用errors='replace'参数处理编码错误
    with open('../data/combined_query_literature.csv', 'r', encoding='utf-8', errors='replace') as file:
        reader = csv.DictReader(file)
        process_file(file, reader)
except UnicodeDecodeError:
    # 如果UTF-8解码失败，尝试使用Latin-1编码
    with open('../data/combined_query_literature.csv', 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        process_file(file, reader)
except FileNotFoundError:
    print("错误: 找不到数据文件 '../data/combined_query_literature.csv'")
    exit(1)
except Exception as e:
    print(f"发生错误: {str(e)}")
    exit(1)

# 计算每个类别内参数的相对权重
category_weights = {}
for category, params in parameter_categories.items():
    category_total = sum(parameter_counts[param] for param in params)
    if category_total > 0:
        category_weights[category] = {param: parameter_counts[param]/category_total for param in params if parameter_counts[param] > 0}

# 计算各类别的权重
total_mentions = sum(category_counts.values())
category_relative_weights = {}
if total_mentions > 0:
    category_relative_weights = {cat: count/total_mentions for cat, count in category_counts.items()}

# 输出年份分布
if years:
    min_year = min(years)
    max_year = max(years)
    year_counts = Counter(years)
    print(f'年份分布: {min_year}-{max_year}')
    year_ranges = [(2000, 2005), (2006, 2010), (2011, 2015), (2016, 2020), (2021, 2025)]
    for start, end in year_ranges:
        count = sum(year_counts[y] for y in range(start, end+1) if y in year_counts)
        print(f'{start}-{end}: {count} 文献')

# 输出类别权重
print('\n类别权重:')
for category, weight in sorted(category_relative_weights.items(), key=lambda x: x[1], reverse=True):
    print(f'{category}: {weight:.3f}')

# 输出参数权重
print('\n参数权重:')
for param, count in sorted(parameter_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
    category = param_to_category.get(param, 'unknown')
    print(f'{param} ({category}): {count}')

# 输出权重矩阵
print('\n权重矩阵:')
print('类别,相对权重,参数,参数权重')
for category, weight in sorted(category_relative_weights.items(), key=lambda x: x[1], reverse=True):
    if category in category_weights:
        cat_params = category_weights[category]
        for param, param_weight in sorted(cat_params.items(), key=lambda x: x[1], reverse=True):
            print(f'{category},{weight:.3f},{param},{param_weight:.3f}')

# 将结果保存到文件
try:
    with open('keyword_weights.csv', 'w', encoding='utf-8') as f:
        f.write('类别,相对权重,参数,参数权重\n')
        for category, weight in sorted(category_relative_weights.items(), key=lambda x: x[1], reverse=True):
            if category in category_weights:
                cat_params = category_weights[category]
                for param, param_weight in sorted(cat_params.items(), key=lambda x: x[1], reverse=True):
                    f.write(f'{category},{weight:.3f},{param},{param_weight:.3f}\n')
except IOError as e:
    print(f"保存结果文件时发生错误: {str(e)}")
except Exception as e:
    print(f"发生未知错误: {str(e)}")
