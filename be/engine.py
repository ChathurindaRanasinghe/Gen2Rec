import csv
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains.retrieval import create_retrieval_chain
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.document_loaders.helpers import detect_file_encodings
from langchain_community.vectorstores import Qdrant
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

from .common import EmbeddingModels, LargeLanguageModels
from .utility import process_template

load_dotenv(".env")


class RecommendationEngine:
    def __init__(self) -> None:
        self._available_embedding_models = list(EmbeddingModels())
        self._available_llms = list(LargeLanguageModels())
        self._embeddings = None
        self._llm = ChatOpenAI(
            model=LargeLanguageModels.OpenAI.GPT_4O, verbose=False, temperature=0
        )
        self._document_content_description = None
        self._vectorstore = None
        self._embeddings_available = os.environ.get("EMBEDDINGS_GENERATED") == "1"
        self._persistent_embeddings_path = os.environ.get("PERSISTENT_EMBEDDINGS_PATH")
        self._collection_name = os.environ.get("EMBEDDINGS_COLLECTION_NAME")
        self._metadata_field_info = None
        self._category = None
        self._retriever_prompt_path = os.environ.get("RETRIEVER_PROMPT_PATH")
        self._retriever_prompt = None
        self._retriever = None
        self._system_prompt = None
        self._recommendation_pipeline = None
        self._chat_history = []
        self._embedding_columns = None
        self._dataset_file_path = None

    @property
    def available_embedding_models(self) -> List[str]:
        return self._available_embedding_models

    @property
    def available_llms(self) -> List[str]:
        return self._available_llms

    @property
    def embeddings(self) -> Embeddings:
        if not self._embeddings:
            raise AttributeError("Embeddings not set.")
        return self._embeddings

    @embeddings.setter
    def embeddings(self, model):
        if self._embeddings:
            raise AttributeError(
                f"Embedding model can be updated only once. Embedding model already exists: {self.embeddings}"
            )

        if model in EmbeddingModels.OpenAI():
            self._embeddings = OpenAIEmbeddings(model=model)
        elif model in EmbeddingModels.VoyageAI():
            self._embeddings = VoyageAIEmbeddings(model=model)
        else:
            raise RuntimeError(
                f"Invalid embedding model. Supported embedding models are: {self.available_embedding_models}"
            )

    @property
    def llm(self) -> BaseChatModel:
        if not self._llm:
            raise AttributeError("Large language model not set.")
        return self._llm

    @llm.setter
    def llm(self, model):
        if model in LargeLanguageModels.OpenAI():
            self._llm = ChatOpenAI(model=model, verbose=False, temperature=0)

        elif model in LargeLanguageModels.MetaAI():
            raise NotImplementedError
        else:
            raise RuntimeError(
                f"Invalid large language model. Supported embedding models are: {self.available_llms}"
            )

    @property
    def document_content_description(self) -> str:
        if not self._document_content_description:
            raise AttributeError("Document content description is not set.")
        return self._document_content_description

    @document_content_description.setter
    def document_content_description(self, description):
        self._document_content_description = description

    @property
    def vectorstore(self):
        # Did not add raise AttributeError since vectorstore status should be checked
        return self._vectorstore

    def initialize_vectorstore(self):
        if self._vectorstore:
            raise AttributeError(
                "Once vectorstore is initialized cannot be re-initialized."
            )
        if not self._persistent_embeddings_path:
            raise AttributeError(
                "Persistent embeddings path not set. Set `PERSISTENT_EMBEDDINGS_PATH`."
            )

        if self._embeddings_available:
            if not self._collection_name:
                raise AttributeError(
                    "Collection name not set. Set `EMBEDDINGS_COLLECTION_NAME`"
                )

            self._vectorstore = Qdrant.from_existing_collection(
                embeddings=self.embeddings,
                path=self._persistent_embeddings_path,
                collection_name=self.collection_name,
            )
        else:
            self.collection_name = self.dataset_file_path.stem
            self._vectorstore = Qdrant.from_documents(
                documents=self.load_dataset(),
                embedding=self.embeddings,
                collection_name=self.collection_name,
                path=self._persistent_embeddings_path,
            )

    @property
    def metadata_field_info(self):
        if not self._metadata_field_info:
            raise AttributeError("Metadata field information not set.")
        return self._metadata_field_info

    @metadata_field_info.setter
    def metadata_field_info(self, info):
        self._metadata_field_info = [AttributeInfo(**attribute) for attribute in info]

    @property
    def category(self):
        if not self._category:
            raise AttributeError("Category not set.")
        return self._category

    @category.setter
    def category(self, value: str):
        if self._category:
            raise AttributeError("Category is immutable once initialized.")

        self._category = value.lower()

    @property
    def retriever_prompt(self):
        if not self._retriever_prompt:
            raise AttributeError("Retriever prompt not set.")
        return self._retriever_prompt

    def create_retriever_prompt(self):
        if not self._retriever_prompt_path:
            raise AttributeError(
                "Retriever prompt path not set. Set `RETRIEVER_PROMPT_PATH`"
            )

        retriever_prompt_content = process_template(
            self._retriever_prompt_path, {"category": self.category}
        )

        self._retriever_prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
                ("system", retriever_prompt_content),
            ]
        )

    @property
    def retriever(self):
        if not self._retriever:
            raise AttributeError("Retriever not initialized.")
        return self._retriever

    def initialize_retriever(self):
        if self._retriever:
            raise AttributeError(
                "Once retriever is initialized cannot be re-initialized."
            )

        while True:
            if not self.vectorstore:
                continue
            break

        self_query_retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=self.vectorstore,
            document_contents=self.document_content_description,
            metadata_field_info=self.metadata_field_info,
            enable_limit=True,
            verbose=False,
        )

        self._retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self_query_retriever,
            prompt=self.retriever_prompt,
        )

    @property
    def system_prompt(self):
        if not self._system_prompt:
            raise AttributeError("System prompt not set.")
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt_content):
        self._system_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_content),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    @property
    def recommendation_pipeline(self):
        if not self._recommendation_pipeline:
            raise AttributeError("Recommendation pipeline not initialized.")

        return self._recommendation_pipeline

    def initialize_recommendation_pipeline(self):
        self.initialize_vectorstore()
        self.initialize_retriever()

        def format_docs(docs):
            return "\n\n".join(
                f"{doc.page_content}\n\nMetadata: {doc.metadata}" for doc in docs
            )

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | self.system_prompt
            | self.llm
            | StrOutputParser()
        )

        self._recommendation_pipeline = create_retrieval_chain(
            self.retriever, rag_chain_from_docs
        )

    @property
    def chat_history(self):
        return self._chat_history

    def run_recommendation_system(self, query: str, recommendation_only: bool = False):
        output = self.recommendation_pipeline.invoke(
            {"input": query, "chat_history": self.chat_history}
        )
        self.recommendation_pipeline.stream()
        if not recommendation_only:
            self.chat_history.extend([HumanMessage(content=query), output["answer"]])
            return output
        else:
            return output["context"]

    @property
    def embedding_columns(self):
        if not self._embedding_columns:
            raise AttributeError("Embedding columns not set.")
        return self._embedding_columns

    @embedding_columns.setter
    def embedding_columns(self, columns: List[str]):
        self._embedding_columns = columns

    @property
    def dataset_file_path(self):
        if not self._dataset_file_path:
            raise AttributeError("Dataset file path not set.")
        return self._dataset_file_path

    @dataset_file_path.setter
    def dataset_file_path(self, path: str | Path):
        if not isinstance(path, Path):
            self._dataset_file_path = Path(path)
        else:
            self._dataset_file_path = path

    @property
    def collection_name(self):
        return self._collection_name

    @collection_name.setter
    def collection_name(self, name: str):
        self._collection_name = name

    def load_dataset(
        self,
    ) -> List[Document]:
        docs = []
        encodings = detect_file_encodings(self.dataset_file_path)
        with open(
            self.dataset_file_path, "r", encoding=encodings[0].encoding
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for index, row in enumerate(reader):
                # TODO: Add improving dataset
                content = ""
                for column in self.embedding_columns:
                    content += f"{column}: {row[column]}\n"

                metadata = {}
                for attribute in self.metadata_field_info:
                    if attribute.type == "string":
                        metadata[attribute.name] = str(row[attribute.name])
                    elif attribute.type == "integer":
                        metadata[attribute.name] = int(row[attribute.name])
                    elif attribute.type == "float":
                        metadata[attribute.name] = float(row[attribute.name])
                metadata["source"] = index
                docs.append(Document(page_content=content, metadata=metadata))

        return docs
