## These are our Repos
from libs.chains import *
from libs.utils import *

## General Utils Repos
import re
from typing import Tuple, Any

## Chainlit Repos
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

## This isn't working as expected (Start should be called on either of these callbacks)
@cl.on_settings_update
@cl.on_chat_start
async def start():
    print("DEBUG: start() called")

    """
    This section reads the default settings from the default_settings.yaml file and sets up the initial settings
    """

    config_file = "./src/default_settings.yaml"
    ## These are the default settings that the user will use, they can change them in the setting button next to the message input text box
    default_settings = read_config_file(config_file)
    chat_settings = await setup_chat_settings(default_settings["settings_data"])
    print(chat_settings)
    print("DEBUG: Chat Setting in start():", chat_settings)
    await update_settings(chat_settings)

    """
    This section reads the default welcome message from the defaults_settings.yaml file and displays the initial welcome message
    """

    welcome_message = cl.Message(content="Starting the bot...")
    await welcome_message.send()

    welcome_message = default_settings["welcome_message"]
    elements = [
        cl.Text(name="Disclaimer and Rules", content=welcome_message, display="inline")
    ]
    """
    This prints the welcome message and sets the default chain based on the chain_selector function
    Eventually, we will move to agents and chain_selector will become obsolete
    """
    await cl.Message(
        content="",
        elements=elements,
    ).send()

    ## Setting the default chain
    # chain = memory_bot(cl.user_session.get("model"))
    chain, chain_type = await chain_selector(chat_settings["chain"])
    print(f"DEBUG: chain_type: {chain_type}")
    cl.user_session.set("chain", chain),
    cl.user_session.set("chain_type", chain_type)

@cl.on_message
async def main(message):
    """
    Processes incoming chat messages.
    """
    chain = cl.user_session.get("chain")

    ## Added stream_final_answer=True to enable nice streaming as we go along

    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
    )
    cb.answer_reached = True
    ## This works with simple_bot() chain
    # result = await chain.acall(message.content, callbacks=[cb])
    ## this works with rag_bot() chain

    ## TODO: This part is broken atm, works for rag_bot but not simple_bot. This works differently with the different chains, we might need an invoke_handler function and a response_handler
    # cl.user_session.get("chain_type") == "rag_bot"

    if cl.user_session.get("chain_type") == "rag_bot":
        print("DEBUG: rag_bot selected")
        result = await chain.ainvoke(message.content, callbacks=[cb])
    else:
        print("DEBUG: memory_bot selected")
        result = await chain.acall(message.content, callbacks=[cb])
    # result = await chain.ainvoke(message.content, callbacks=[cb])

    # print(f"DEBUG: result from chain: {result}")
    answer = result["response"]

    text_elements = []  # type: List[cl.Text]
    unique_sources = set()
    for element in result["context"]:
        # print("ELEMENT:::", element)
        # print("\n\n Page Content::: \n ",element.page_content)
        source = element.metadata["source"]
        ## TODO: need to remove this part, users will not need this, it's good for debug.
        formatted_content = re.sub(r"\n", " ", element.page_content)
        formatted_content = re.sub(r"\.", ".\n", formatted_content)
        page_content = formatted_content
        text_elements.append(
            cl.Text(content=page_content, name=source, display="inline")
            # Bad line cl.Text(url=source, name=source, display="inline")
        )

    await cl.Message(content=answer, elements=text_elements).send()


@cl.on_settings_update
async def update_settings(chat_settings):
    print("DEBUG: on_settings_update", chat_settings)
    for key, value in chat_settings.items():
        print(f"Setting Key: {key}, Value: {value}")
        cl.user_session.set(key, value)
    cl.user_session.set("chain", await chain_selector(chat_settings["chain"]))

async def chain_selector(selected_chain) -> Tuple[Any, str]:
    print("DEBUG:chain_selector:", selected_chain)
    if selected_chain == "Simple Chatbot":
        print("memory_bot selected")
        chain = memory_bot(cl.user_session.get("model"))
        chain_type = "memory_bot"
        return chain, chain_type

    elif selected_chain == "Sales RAG Chatbot":
        print("Sales RAG Chatbot selected")
        chain = rag_bot(cl.user_session.get("model"))
        chain_type = "rag_bot"
        return chain, chain_type

    # else:
    #     print("Default action")
    #     chain = memory_bot(cl.user_session.get("model"))
    #     chain_type = "rag_bot"
    #     return chain, chain_type