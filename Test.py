import pandas as pd
import os
from utils import process_a_file

def main():

    file_path = "./Test1.xlsx"
    output = process_a_file(file_path)
    print(output)
    assert list(output.columns) == ['地区','Year', 'Test1']
    #assert set(output['地区'].contains(['上海市']))
    assert '上海市' in output['地区'].values
    assert pd.api.types.is_numeric_dtype(output['Test1'])

    hunan_2023 = output.query(" 地区 == '湖南省' and Year == 2023")['Test1'].values[0]
    assert hunan_2023 == 2782
    print("牛啊!")

    output.to_csv('Test1_processed.csv', encoding='utf-8')

if __name__ == "__main__":
    main()