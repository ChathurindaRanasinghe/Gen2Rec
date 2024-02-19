import os
import re
import json
from pprint import pprint

import pinecone
import icecream as ic
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Pinecone, Qdrant
from langchain_community.vectorstores.redis import Redis

from prompts import recommendation_engine_prompt
from utility.token_counter import count_tokens


def get_vectorstore_from_csv(*, path: str, index_name: str, vector_store: str = "qdrant"):
    if vector_store == "redis":
        loader = CSVLoader(path)
        data = clean_data(loader.load())
        print(f"token count = {sum(count_tokens(model='gpt-3.5-turbo', text=doc.page_content) for doc in data)}")
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        return Redis.from_documents(
            documents=data,
            embedding=embeddings,
            redis_url="redis://localhost:6379",
            index_name=index_name
        )

    if vector_store == "qdrant":
        loader = CSVLoader(path)
        data = clean_data(loader.load())
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        return Qdrant.from_documents(
            data,
            embeddings,
            url="0.0.0.0:6333",
            prefer_grpc=True,
            collection_name=index_name,
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


def main():

    load_dotenv(dotenv_path="./.env")
    vectorstore = get_vectorstore_from_csv(path="./laptop.csv", index_name="demo-laptop")

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            verbose=True,
            streaming=False,
            temperature=0.2,
        ),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
        chain_type_kwargs={"prompt": recommendation_engine_prompt},
        return_source_documents=True,
    )

    while True:
        user_query = input("Enter Query: ").strip()
        if user_query == "q":
            break
        result = qa_chain.invoke(input=user_query)
        pprint(result['result'])


if __name__ == "__main__":
    main()
