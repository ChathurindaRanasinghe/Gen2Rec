import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import FAISS


def get_embeddings_from_csv(path: str):
    loader = CSVLoader("Example CSV")
    documents = loader.load()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
