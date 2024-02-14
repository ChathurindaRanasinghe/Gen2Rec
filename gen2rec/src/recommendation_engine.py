import os
import re
from pprint import pprint

import icecream as ic  # noqa: F401
import pinecone
import redis
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Pinecone
from langchain_community.vectorstores.redis import Redis
from langchain_openai import OpenAIEmbeddings

from gen2rec.src.prompts import recommendation_engine_prompt
from gen2rec.utility.token_counter import count_tokens


def get_vectorstore_from_csv(*, path: str, index_name: str, vector_store: str = "redis"):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.environ.get("OPENAI_API_KEY"))
    if vector_store == "redis":
        print("using redis")
        redis_schema = f"./{index_name}.yaml"
        redis_url = "redis://localhost:6379"
        r = redis.Redis(host="localhost", port=6379, decode_responses=True)

        try:
            r.ft(index_name).info()
            print('index found')
            return Redis.from_existing_index(
                embedding=embeddings,
                index_name=index_name,
                schema=redis_schema,
                redis_url=redis_url
            )

        except Exception as _:
            print('index not available')
            loader = CSVLoader(path)
            data = clean_data(loader.load())
            
            rds = Redis.from_documents(
                documents=data, embedding=embeddings, redis_url=redis_url, index_name=index_name
            )
            rds.write_schema(redis_schema)
            return rds

    if vector_store == "pinecone":
        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment=os.environ.get("PINECONE_ENVIRONMENT"),
        )

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
        # pprint(doc.page_content)
    return data


def main():
    load_dotenv(dotenv_path="./.env")
    vectorstore = get_vectorstore_from_csv(path="./fixed2.csv", index_name="demo2")
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            verbose=True,
            streaming=False,
            temperature=0.7,
        ),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": recommendation_engine_prompt},
    )

    while True:
        user_query = input("Enter Query: ").strip()
        if user_query == "q":
            break
        result = qa_chain.run(query=user_query)
        pprint(result)


if __name__ == "__main__":
    main()
