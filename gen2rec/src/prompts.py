from langchain.prompts import PromptTemplate

RECOMMENDATION_ENGINE_PROMPT_FOOTER = """
Assume you are a laptop reviewer. You task is to recommend laptops to user based on the requirements.
Provide laptop model & brand.
Please provide your explanation to your recommendation.

EXAMPLE:
GIGABYTE G6 KF-H3US853SH
END OF EXAMPLE


CONTEXT: {context}

QUESTION: {question}

Helpful Answer"""
recommendation_engine_prompt = PromptTemplate(
    template=RECOMMENDATION_ENGINE_PROMPT_FOOTER, input_variables=['context', 'question']
)

NEWS_ENGINE = """
Assume you are a news recommendation system. You need to recommend news according to user interesets from the provided news data.
CONTEXT: {context}

QUESTION: {question}

Helpful Answer"""

news_prompt = PromptTemplate(
    template=NEWS_ENGINE, input_variables=['context', 'question']
)

# Can you recommend me a laptop for video editing