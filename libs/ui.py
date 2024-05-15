import config as cfg
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from libs.ai import setup_chain
from langchain.schema.runnable.config import RunnableConfig


@cl.on_chat_start
async def on_chat_start():
    await setup_chat_settings()
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

async def setup_chat_settings():
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
    # await setup_agent(settings)
