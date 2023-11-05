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

os.system(f"sqlite3 db.{db_name}.db '.dump{table_name}' > {table_name}.sql")
# 读取 SQLite 数据库中的表 table_name 中的表头并打印
cursor = conn.cursor()
cursor.execute(f"SELECT \"University\" FROM {table_name}")
print(cursor.description)

# 导出表格
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
print(df)

# 关闭数据库连接
#conn.close()
''' 创建SQL语句
create_table_statement = f"CREATE TABLE {table_name} ({', '.join(column_names)}) IF NOT EXISTS;\n"
print(create_table_statement)
conn.execute(create_table_statement)'''
# 生成插入数据的SQL语句
insert_values = []
for _, row in df.iterrows():
    values = row.tolist()
    formatted_values = [f"'{v}'" if isinstance(v, str) else str(v) for v in values]
    insert_sentence = f"INSERT INTO {table_name} VALUES ({', '.join(formatted_values)});\n"
    conn.execute(insert_sentence)
    insert_values.append(insert_sentence)
insert_data_statement = ''.join(insert_values)


# 写入SQL文件
'''with open('output.sql', 'w') as f:
    f.write(create_table_statement)
    f.write(insert_data_statement)'''