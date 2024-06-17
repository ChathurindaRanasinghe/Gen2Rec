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

from prompts import news_prompt
from utility.token_counter import count_tokens


def get_vectorstore_from_csv(*, path: str, index_name: str, vector_store: str = "qdrant"):
    if vector_store == "redis":
        loader = CSVLoader(path)
        data = loader.load()
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
        data = loader.load()
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
            data = loader.load()
            print(f"token count = {sum(count_tokens(model='gpt-3.5-turbo', text=doc.page_content) for doc in data)}")
            pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
            return Pinecone.from_documents(documents=data, embedding=embeddings, index_name=index_name)



def main():

    load_dotenv(dotenv_path="./.env")
    vectorstore = get_vectorstore_from_csv(path=f"./news.csv", index_name="news")
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            verbose=True,
            streaming=False,
            temperature=0.2,
        ),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": news_prompt},
        return_source_documents=True,
    )


    user_query = "I am interested in global politics. LOCATION: UK, DATE: 2018 November"
    result = qa_chain.invoke(input=user_query)
    pprint(result['result'])

if __name__ == "__main__":
    main()
