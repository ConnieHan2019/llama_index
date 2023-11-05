import logging
import os
import sys

import openai

from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import ServiceContext
from llama_index.llms import PaLM

if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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"
    openai.api_key = os.environ["OPENAI_API_KEY"]

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # openai.log = "debug"

    service_context = ServiceContext.from_defaults()
    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    # define a workflow for the query engine
    query_engine = index.as_query_engine(similarity_top_k=5, service_context=service_context,
                                         response_mode="tree_summarize")
    response = query_engine.query("What did the author do growing up?")
    print(response)

    # response = query_engine.query("What's the url of Visual Arts & Sound Art Department in Columbia University?")
    # print(response)
    #
    # response = query_engine.query(
    #     "How many schools are there in Johns Hopkins University? Please give me the accurate number and their names")
    # print(response)

    # response = query_engine.query(
    #     "清华大学有哪些学院和专业？请给出详细的数量并列举出它们的名字")
    # print(response)
    #
    # response = query_engine.query(
    #     "北京大学有哪些专业，它们的学费分别是多少，超过12000的有多少")
    # print(response)

    # response = query_engine.query(
    #     "北京大学有哪些专业，学费前三的专业是哪些，学制前三长的专业是哪些，所有专业的平均学费是多少？")
    # print(response)

    # query_engine = index.as_query_engine(service_context=service_context)
    # response = query_engine.query("帮我生成具有年轻化气息的10个社交账号昵称，不超过6个汉字或12个英文字母")
    # print(response)
    #
    # response = query_engine.chat("Oh interesting, tell me more.")
    # print(response)
