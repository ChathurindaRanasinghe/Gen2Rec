from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import Document
from pydantic import BaseModel, Field


# class Recommendation(BaseModel):
#     result: list = Field(description="news recommendation results given")
#     # context: List[Document] = Field(description="list of documents used")


def check_recommendation_with_document(recommendation_doc) -> bool:
    # model = ChatOpenAI(temperature=0, openai_api_key="")
    #
    # parser = PydanticOutputParser(pydantic_object=Players)
    #
    # # ---------------------------- SETUP THE REQUEST -----------------------------
    # human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
    # chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
    #
    # request = chat_prompt.format_prompt(
    #     request='Give me facts about 2 NBA players around the world',
    #     format_instructions=parser.get_format_instructions()
    # ).to_messages()
    #
    # results = model(request, temperature=0)
    # print(results)
    # results_values = parser.parse(results.content)  # Player class object
    # print(results_values)

    # model = ChatOpenAI(temperature=0,openai_api_key="")
    # parser = PydanticOutputParser(pydantic_object=Recommendation)

    # prompt = PromptTemplate(
    #     template="Answer the user query.\n{format_instructions}\n{query}\n",
    #     input_variables=["query"],
    #     partial_variables={"format_instructions": parser.get_format_instructions()},
    # )
    # results = parser.parse(recommendation_doc)
    # print(results)

    # output=model.invoke(prompt)

    # chain = prompt | model | parser

    # chain.invoke({"query": recommendation_doc['query']})
    # output=parser.parse("MSI GL63 8RC")
    # print(output)

    # keywords = recommendation_doc["source_documents"]
    # texts = recommendation_doc["result"]
    # keywords_set = set(keywords.split())
    # texts_set = set(texts.split())
    # if texts_set.issubset(keywords_set):
    return True
    # return False


def evaluate_recommendation(recommendation_doc) -> bool:
    if check_recommendation_with_document(recommendation_doc):
        return True


class Recommendation(BaseModel):
    recommendation: str = Field(description='Name of the laptop')
    explanation: str = Field(description='Explanation for choosing the laptop')
    document: str = Field(description='Documents referred to give the recommendation')


class RecommendationDoc(BaseModel):
    recommendations: list[Recommendation] = Field(description='Python list of Recommendation objects containing '
                                                              'laptop model and explanation and documents referred')


if __name__ == "__main__":
    model = ChatOpenAI(temperature=0, openai_api_key="")

    human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])

    parser = PydanticOutputParser(pydantic_object=RecommendationDoc)

    request = chat_prompt.format_prompt(
        request='Give me laptops suitable for gaming and give the explanation too',
        format_instructions=parser.get_format_instructions()
    ).to_messages()

    results = model(request, temperature=0)
    results_values = parser.parse(results.content)
    print(results_values)

    # recommendations = [{'laptop_model': 'ASUS ROG Zephyrus G14',
    #                     'explanation': 'This laptop is equipped with a powerful AMD Ryzen 9 processor and NVIDIA GeForce RTX 2060 graphics card, making it suitable for gaming. It also has a high refresh rate display and good battery life for gaming on the go.',
    #                     'documents_referred': ['https://www.asus.com/Laptops/ROG-Zephyrus-G14/']},
    #                    {'laptop_model': 'MSI GS66 Stealth',
    #                     'explanation': 'The MSI GS66 Stealth features an Intel Core i7 processor and NVIDIA GeForce RTX 2070 Super graphics card, providing excellent performance for gaming. It also has a sleek design and good cooling system for long gaming sessions.',
    #                     'documents_referred': ['https://www.msi.com/Laptop/GS66-Stealth-10SX']}]
