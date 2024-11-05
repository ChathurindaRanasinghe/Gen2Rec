import csv
import json
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_core.documents.base import Document
from langchain_voyageai import VoyageAIEmbeddings
from loguru import logger

from be.common import EmbeddingModels

load_dotenv(".env")


def load_dataset(
        dataset_file_path: str, metadata_field_info: list
) -> List[Document]:
    docs = []
    metadata_columns = [attribute["name"] for attribute in metadata_field_info]
    with open(dataset_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for index, row in enumerate(reader):
            print(index, end="\r")
            content = ""
            for column in row:
                if column not in metadata_columns:
                    content += f"{column}: {row[column]}\n"

            metadata = {}
            for attribute in metadata_field_info:
                if attribute["type"] == "string":
                    metadata[attribute["name"]] = str(row[attribute["name"]])
                elif attribute["type"] == "integer":
                    metadata[attribute["name"]] = int(row[attribute["name"]])
                elif attribute["type"] == "float":
                    metadata[attribute["name"]] = float(row[attribute["name"]])
            metadata["source"] = index
            docs.append(Document(page_content=content, metadata=metadata))

            if index == 10000:
                break

    return docs


def main():
    metadata_json_path = "news_metadata.json"
    with open(metadata_json_path, "r") as f:
        metadata_info = json.load(f)

    documents = load_dataset(
        dataset_file_path="news_dataset.csv",
        metadata_field_info=metadata_info,
        # chain=description_generation_chain,
    )
    # print(documents[0])
    logger.info("Loading dataset is completed. Generating embeddings.")

    Qdrant.from_documents(
        documents=documents,
        embedding=VoyageAIEmbeddings(
            model=EmbeddingModels.VoyageAI.VOYAGE_LARGE_2_INSTRUCT,
            voyage_api_key=os.environ.get("VOYAGE_AI_API_KEY"),
        ),
        collection_name="news",
        path=os.environ.get("PERSISTENT_EMBEDDINGS_PATH"),
    )


if __name__ == "__main__":
    main()
