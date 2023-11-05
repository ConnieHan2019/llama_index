import os
import openai
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column, text,
)
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    SQLDatabase,
    ServiceContext,
)
from llama_index.llms import OpenAI
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.tools import QueryEngineTool



os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]
engine = create_engine("sqlite:///uni.db", future=True)
# 从dump.sql文件中读取SQL语句，并通过engine执行
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)
# 读取SQL文件内容
with open('dump.sql', 'r') as file:
    sql_script = file.read()
    #sql_script = sql_script.replace(":", r"\:")

statements = sql_script.split(';')
# 执行SQL脚本
with engine.connect() as connection:
    for statement in statements:
        # 去除语句两端的空格
        statement = statement.strip().replace(":", r"\:").replace("\n", "")
        if statement:
            try:
                connection.execute(text(statement))
            except Exception as e:
                print(f"执行语句出错: {statement}")
                print(f"错误信息: {str(e)}")
    connection.commit()
#connection.execute(text(sql_script))
sql_database = SQLDatabase(engine, include_tables=["american_universities"])
sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["american_universities"],
)

print("start to query")
response = sql_query_engine.query("How many universities are there in the table?")
print(response)
'''sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description=(
        "Useful for translating a natural language query into a SQL query over a table containing: "
        "american_universities,containing  University ,  Schools web ,  School ,   Department ,  "
        " Department Web ,  Program list Web ,  Major ,  Program Web ,  Duration ,  Admission requirement Web , "
        " Deadline ,  Remark  "
    ),
)'''