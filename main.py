import h5py
import pandas as pd
import numpy as np
from tqdm import tqdm  # 确保这样正确导入

filename = 'name.hdf5' # 文件路径
output_name = filename[:-5]
dataset_path = "" # HDF5文件中的数据集路径
f = h5py.File(filename, 'r') # 只读方式打开文件

n = len(f.keys())
dirs = list(zip(range(n), list(f.keys())))
print(dirs)
x = 0
while True:
    print("请选择您要导出的文件编号")
    x = int(input())
    if not(0 <= x < n):
        print("选择错误, 请您重新选择")
        continue
    else:
        dataset_path = dirs[x][1]
        print("成功选择, 数据集为:", dataset_path)
        break

print("导出成csv文件开始")
if dataset_path in f:
    dataset = f[dataset_path] # 选择对应的数据集
    max_length = max(len(dataset[table_name]['Value'][:]) for table_name in dataset.keys())
    data_dict = {}
    for table_name in tqdm(dataset, desc="Processing tables"): # 获取该数据集下所有的列表
        values = dataset[table_name]['Value'][:] # 获取所有的值
        values = values.astype(str)  # 确保所有数据都是字符串格式

        # 使用""填充到最大长度，这样转换为DataFrame后将自动转为空字符串
        padded_values = np.pad(values, (0, max_length - len(values)), mode='constant', constant_values="")
        data_dict[table_name] = padded_values # 保存到字典中

    df = pd.DataFrame(data_dict) # 转成DataFrame格式

    # 导出到CSV文件
    csv_filename = output_name + '.csv'
    df.to_csv(csv_filename, index=False)
    print(f'Data exported to {csv_filename}')
