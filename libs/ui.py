import config as cfg
import chainlit as cl
from libs.ai import setup_chain
from langchain.schema.runnable.config import RunnableConfig


@cl.on_chat_start
def on_chat_start():
    chain = setup_chain()                                   # Setup the chain
    cl.user_session.set("chain", chain)                     # Save the chain to the chainlit user session


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