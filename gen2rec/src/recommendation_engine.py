import json
from operator import index
import os
import re
from pprint import pprint
from time import perf_counter

import icecream as ic
import pinecone
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.vectorstores.redis import Redis
from langchain_community.vectorstores.pinecone import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import redis

from gen2rec.src.prompts import recommendation_engine_prompt, book_recommendation_prompt_template
from gen2rec.utility.token_counter import count_tokens
from qdrant_client import QdrantClient



def get_vectorstore_from_csv(*, path: str, index_name: str, vector_store: str = "qdrant"):
    if vector_store == "redis":
        r = redis.Redis(decode_responses=True)
        encoding = "utf-8"
        if index_name == "demo-book":
            encoding = "latin1"
        loader = CSVLoader(path, encoding=encoding)
        if index_name == "demo-laptop":
            data = clean_data(loader.load())
        else:
            data = loader.load()
        # print(f"token count = {sum(count_tokens(model='gpt-3.5-turbo', text=doc.page_content) for doc in data)}")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        indexes = r.keys()
        # print(f"{indexes=}")
        for key in indexes:
            if index_name in key:
                print("Getting from existing index")
                return Redis.from_existing_index(embedding=embeddings, index_name=index_name, schema=f"{index_name}.yaml",redis_url="redis://localhost:6379")    
        
        rds = Redis.from_documents(
            documents=data, embedding=embeddings, redis_url="redis://localhost:6379", index_name=index_name
        )
        rds.write_schema(f"{index_name}.yaml")
        return rds

    if vector_store == "qdrant":
        # client = QdrantClient("localhost", port=6333)
        # collections = client.get_collections()
        encoding = "utf-8"
        if index_name == "demo-book":
            encoding = "latin1"
        loader = CSVLoader(path, encoding=encoding)
        if index_name == "demo-laptop":
            data = clean_data(loader.load())
        else:
            data = loader.load()
        print("loaded data")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        print("got embeddings")
        return Qdrant.from_documents(
            data,
            embeddings,
            url="0.0.0.0:6333",
            prefer_grpc=True,
            collection_name=index_name,
            force_recreate=False
        )

    if vector_store == "pinecone":
        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment=os.environ.get("PINECONE_ENVIRONMENT"),
        )

        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        if index_name in pinecone.list_indexes():
            return Pinecone.from_existing_index(index_name, embeddings)
        else:
            loader = CSVLoader(path)
            data = clean_data(loader.load())
            print(f"token count = {sum(count_tokens(model='gpt-3.5-turbo', text=doc.page_content) for doc in data)}")
            pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
            return Pinecone.from_documents(documents=data, embedding=embeddings, index_name=index_name)


def clean_data(data):
    pattern = re.compile(r"([^:]+:\s*(?:\n|$))")
    for doc in data:
        doc.page_content = pattern.sub("", doc.page_content)
        doc.page_content = "\n".join(doc.page_content.split("\n")[1:])
    return data


class Dataset:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path


def load(dataset):

    load_dotenv(dotenv_path="./.env")
    vectorstore = get_vectorstore_from_csv(path=f"./{dataset}.csv", index_name=f"demo-{dataset}", vector_store="redis")

    if dataset == "laptop":
        prompt = recommendation_engine_prompt
    if dataset == "book":
        prompt = book_recommendation_prompt_template

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            verbose=True,
            streaming=False,
            temperature=0.2,
        ),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return qa_chain

if __name__ == '__main__':
    load("laptop")
    load("book")
