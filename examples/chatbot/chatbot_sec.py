from llama_index import ListIndex, LLMPredictor
from llama_index.llms import OpenAI
from llama_index.indices.composability import ComposableGraph
from llama_index import download_loader, VectorStoreIndex, ServiceContext
from pathlib import Path

# set summary text for each doc
years = [2022, 2021, 2020, 2019]
UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)
loader = UnstructuredReader()
doc_set = {}
all_docs = []
for year in years:
    year_docs = loader.load_data(
        file=Path(f"/Users/mingluhan/PycharmProjects/llama_index/docs/examples/data/UBER/UBER_{year}.html"), split_documents=False
    )
    # insert year metadata into each year
    for d in year_docs:
        d.metadata = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)


# initialize simple vector indices + global vector index
# NOTE: don't run this cell if the indices are already loaded!
index_set = {}
service_context = ServiceContext.from_defaults(chunk_size=512)
for year in years:
    cur_index = VectorStoreIndex.from_documents(
        doc_set[year], service_context=service_context
    )
    index_set[year] = cur_index
# Load indices from disk
#index_set = {}
#for year in years:
#    index_set[year] = cur_index



index_summaries = [f"UBER 10-k Filing for {year} fiscal year" for year in years]
# set number of output tokens
llm = OpenAI(temperature=0, max_tokens=512, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)


# set summary text for each doc
index_summaries = [f"UBER 10-k Filing for {year} fiscal year" for year in years]


# define a list index over the vector indices
# allows us to synthesize information across each index
graph = ComposableGraph.from_indices(
    ListIndex,
    [index_set[y] for y in years],
    index_summaries=index_summaries,
    service_context=service_context,
)