from config import *
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema import StrOutputParser

from loguru import logger
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

#    logger.info(f"INFO: entering function: {function}")

# logger.info(f"INFO: exciting function: {function}")

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
        ]
    )
    return prompt


def setup_chain():
    llm = setup_llm()
    prompt = setup_prompt()
    chain = ( prompt 
        | llm 
        | StrOutputParser()
    )
    return chain
