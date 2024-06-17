from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationSummaryMemory
from dotenv import load_dotenv
import os


template = """The following is a friendly conversation between a human and an AI. The AI is an expert in laptops. AI asks questions from the human based on his needs to select a suitable laptop. Ask NO MORE than 5 questions
DO NOT ask technical questions. Assume you user have no idea about technical details.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

load_dotenv(dotenv_path="./.env")

llm = ChatOpenAI(temperature=0.6, openai_api_key=os.environ.get("OPENAI_API_KEY"), model_name="gpt-3.5-turbo")

SUMMARY_PROMPT = """
Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary.
Capture the user needs & requirements focus on them.

EXAMPLE
Current summary:
User wants to buy a laptop.

New lines of conversation:
AI: For what purposes will you use this laptop?
User: I am a videographer, I will mainly use this laptop for video editing.

New summary:
User is a videgrapher who will use the laptop mainly for video editing.
END OF EXAMPLE

Current summary:
{summary}

New lines of conversation:
{new_lines}

New summary:
"""

summary_prompt_template = PromptTemplate(template=SUMMARY_PROMPT, input_variables=["summary", "newline"])


conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    # verbose=True,
    memory=ConversationSummaryMemory(
        ai_prefix="AI Assistant", human_prefix="User", llm=llm, prompt=summary_prompt_template
    ),
)

entry = "1"

while entry != "q":
    entry = input("Query: ")
    print(conversation.predict(input=entry))

conversation_summary = conversation.memory.buffer
