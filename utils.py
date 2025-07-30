# The one yh try to build from scratch (with the help of AI)


import os
import pandas as pd
import re

pat = r'^\s*((?:20)\d{2})'
interest_years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

def read_files(files_path):
   for file in os.listdir(files_path):
        if file.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(files_path, file))
            var_name = os.path.splitext(file)[0] 
            # TO DO

def find_year_cols(df):
    year_cols = []
    for col in df.columns:
        m = re.match(pat, str(col))
        if m:
            year_cols.append(col)
    return year_cols

def reg_col_name(df) -> pd.DataFrame:
    col_names = df.columns.tolist()
    for col in df.columns:
        if col == '' or pd.isna(col):
            df.drop(columns=col, inplace=True)
            col_names.remove(col) # 去掉空列
        if col == '地区':
            continue
        m = re.match(pat, str(col))
        if m:
            #col_names[col]
            col_names[col_names.index(col)] = m.group(1)  # 用索引修改列名
    df.columns = col_names
    return df


def process_a_file(file_path):
    var_name = os.path.splitext(os.path.basename(file_path))[0]  # 获取不带扩展名的文件名
    original_df = pd.read_excel(file_path)
    df = reg_col_name(original_df)
    #df = df.loc[:, interest_years]

    #地区列本来就是竖着的，保持不动
    #找出年份列
    year_cols = find_year_cols(df)
    
    #使用 melt 将年份列由横着转化为竖着
    new_df = df.melt(id_vars=['地区'], value_vars=year_cols, var_name='Year', value_name=var_name)
    # 把年份中的'2019'转化为整数
    new_df['Year'] = pd.to_numeric(new_df['Year'], errors='coerce').astype('Int64')
    return new_df


def Merge_to_one(files_path) -> pd.DataFrame:
    #merged_df = pd.DataFrame()
    merged_df = None
    for file in os.listdir(files_path):
        if file.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(files_path, file))
            new_df = process_a_file(os.path.join(files_path, file))
            #merged_df = pd.combine(merged_df, new_df, how='outer', on=['地区', 'Year'])
            #用combine是错的呀，combime是逐元素合并两个表
            if merged_df is None:
                merged_df = new_df
            else:
                merged_df = pd.merge(merged_df, new_df, on=['地区', 'Year'], how='outer')
    return merged_df


def map_to_eng(df) -> pd.DataFrame:
    mapping = {
        '地区': 'Province',
        '上海市': 'Shanghai',
        '湖南省': 'Hunan',
        '北京市': 'Beijing',
        '广东省': 'Guangdong',
        '江苏省': 'Jiangsu',
        '浙江省': 'Zhejiang',  
        '山东省': 'Shandong',
        '河南省': 'Henan',
        '河北省': 'Hebei',
        '四川省': 'Sichuan',
        '湖北省': 'Hubei',
        '陕西省': 'Shaanxi',
        '甘肃省': 'Gansu',
        '福建省': 'Fujian',
        '安徽省': 'Anhui',
        '天津市': 'Tianjin',
        '重庆市': 'Chongqing',
        '云南省': 'Yunnan',
        '广西壮族自治区': 'Guangxi',
        '内蒙古自治区': 'Inner Mongolia',
        '吉林省': 'Jilin',
        '黑龙江省': 'Heilongjiang',
        '辽宁省': 'Liaoning',
        '山西省': 'Shanxi',
        '贵州省': 'Guizhou',
        '西藏自治区': 'Tibet',
        '宁夏回族自治区': 'Ningxia',
        '青海省': 'Qinghai',
        '新疆维吾尔自治区': 'Xinjiang',
        '海南省': 'Hainan',
    }
    # 检查 DataFrame 是否包含需要映射的中文
    df = df.replace(mapping)
    return df
