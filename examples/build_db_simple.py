import os
import sqlite3

import pandas as pd
import numpy as np

# 读取XLSX文件，跳过空行
#df = pd.read_excel('/Users/mingluhan/PycharmProjects/llama_index/examples/美国查校表格(无图片版本）.xlsx', skiprows=lambda x: x > 0 and all(pd.isna(i) for i in x))
df = pd.read_excel('/Users/mingluhan/PycharmProjects/llama_index/examples/美国查校表格(无图片版本）.xlsx')
print(df.shape)
# 删除整行为空的行
df.dropna(how='all', inplace=True)
print(df.shape)
# 填充第一列的空值
df['University'].fillna(method='ffill', inplace=True)

# 转换为SQL表格
table_name = 'american_universities'
db_name = 'uni'
column_names = df.columns.tolist()
print(column_names)
# 连接到 SQLite 数据库
conn = sqlite3.connect('uni.db')

# 将数据保存到 SQLite 数据库中的表 table_name 中
df.to_sql(table_name, conn, if_exists='replace', index=False)

# 导出sqlite数据库的表格

with open('dump.sql', 'w') as f:
    for line in conn.iterdump():
        f.write('%s\n' % line)
conn.close()

