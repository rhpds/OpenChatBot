import config as cfg
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from libs.ai import setup_chain
from langchain.schema.runnable.config import RunnableConfig
from loguru import logger
import sys

@cl.on_chat_start
async def on_chat_start():
    settings = await setup_chat_settings()
    # logger.setLevel(logging.INFO)  # Set level to INFO, so DEBUG messages are ignored
    # logger.info(f"Model: {settings['Model']}, Chains: {settings['Chains']}, Streaming: {settings['Streaming']}, Temperature: {settings['Temperature']}")
    # logger.remove()  # Remove default handler
    # logger.add(sys.stdout, level=settings["logging_level"], format="{time} {level} {message} (Function: {function})")
    # logger.add("logfile.log", level="INFO", format="{time} {level} {message} (Function: {function})")
    # logger.info("This info message will be shown.")
    chain = setup_chain()                                   # Setup the chain
    cl.user_session.set("chain", chain)                     # Save the chain to the chainlit user_session


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")                    # 1. Retreive chain from user session
    msg = cl.Message(content="")

    async for chunk in chain.astream(                       # 2. Run the chain aynchronously
        {"question": message.content, "system_persona": cfg.SYSTEM_PERSONA},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

async def setup_chat_settings():
    """
    Setup the chat settings, everything else from config.py
    """
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Ollama - Model",
                values=[
                    "mistral",
                    "llama2"
                ],
                initial_index=0,
            ),
            Select(
                id="logging_level",
                label="Logging Level",
                values=[
                    "DEBUG",
                    "INFO",
                    "WARNING",
                    "ERROR",
                    "CRITICAL",
                ],
                initial_index=1,
            ),
            Select(
                id="Chains",
                label="Chains",
                values=["chatbot_llm", "chabot_rag"],
                initial_index=1,
            ),
            Switch(
                id="Streaming",
                label="Stream Tokens",
                initial=True,
            ),
            Slider(
                id="Temperature",
                label="Ollama - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
    return settings
    # await setup_agent(settings)
