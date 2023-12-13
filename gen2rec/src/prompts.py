from langchain.prompts import PromptTemplate

RECOMMENDATION_ENGINE_PROMPT_TEMPLATE = """
    Assume you are a laptop reviewer. You task is to recommend laptop from given laptop data based 
    on user requirements. User requirements will be provided in the context.
    Please explain the recommendation.

    {context}

    Question: {question}
    """
recommendation_engine_prompt = PromptTemplate(
    template=RECOMMENDATION_ENGINE_PROMPT_TEMPLATE, input_variables=['context', 'question']
)
