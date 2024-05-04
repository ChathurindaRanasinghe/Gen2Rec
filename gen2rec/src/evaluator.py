from langchain.output_parsers import PydanticOutputParser
from pydantic.v1 import BaseModel, Field


class Recommendation(BaseModel):
    recommendation: str = Field(description="recommendation given")
    context = Field(description="list of documents used")


def check_recommendation_with_document(recommendation_doc) -> bool:
    parser = PydanticOutputParser(pydantic_object=Recommendation)

    keywords = recommendation_doc["context"]
    texts = recommendation_doc["answer"]
    keywords_set = set(keywords.split())
    texts_set = set(texts.split())
    if texts_set.issubset(keywords_set):
        return True
    return False


def evaluate_recommendation(recommendation_doc) -> bool:
    if check_recommendation_with_document(recommendation_doc):
        return True

# output and doc check
