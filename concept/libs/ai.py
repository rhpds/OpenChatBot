from config import *

# from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

# from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema.runnable.config import RunnableConfig
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import StrOutputParser

# from loguru import logger
"""
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
"""

MODEL = "mistral"
# MODEL = "sroecker/granite-7b-lab"

system_persona = "You are a helpful AI assistant that can answer any question. Explain your reasoning and provide sources when possible."


def setup_llm():
    llm = ChatOllama(
        model=MODEL,
    )
    return llm


def setup_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_persona}"),
            ("human", "{question}"),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )
    return prompt


def setup_chain():
    llm = setup_llm()
    prompt = setup_prompt()

    chain = prompt | llm | StrOutputParser()

    chat_history_for_chain = ChatMessageHistory()
    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history_for_chain,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return chain_with_message_history, chat_history_for_chain
