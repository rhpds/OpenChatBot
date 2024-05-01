import os
import config as cfg

# from templates.htmlTemplates import css, bot_template, user_template
from htmlTemplates import css, bot_template, user_template


import random
import streamlit as st
from datetime import datetime


# decorator
def enable_chat_history(func):
    # to clear chat history after swtching chatbot
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    avatar = (
        "https://avatars.dicebear.com/api/avataaars/1.svg"
        if "user" == "user"
        else "https://avatars.dicebear.com/api/avataaars/2.svg"
    )
    # to show chat history on ui

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
        # st.chat_message(msg["role"], avatar="🧑‍💻"):
        #     st.write(msg["content"])

    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    # for messages in st.session_state.messages:
    #     avatar = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Red_Hat_logo.svg/2560px-Red_Hat_logo.svg.png" #"https://cloudassembler.com/images/avatar.png" #... # decide which avatar you want for this message
    # with st.chat_message(messages["role"], avatar=avatar):
    #     st.markdown(messages["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append(
        {
            "role": author,
            "content": msg,
            "avatar": "https://avatars.dicebear.com/api/avataaars/1.svg"
            if author == "user"
            else "https://avatars.dicebear.com/api/avataaars/2.svg",
        }
    )
    st.chat_message(author).write(msg)


def setup_streamlit():
    """
    Function to setup streamlit titles etc configurations
    """
    st.sidebar.title("OpenChatBot")
    st.sidebar.write(
    """
    ## GitHub Repository

    [![view source code ](https://img.shields.io/badge/GitHub%20Repository-gray?logo=github)](https://github.com/rhpds/OpenChatBot.git)

    ## Disclaimer

    **Internal use only - Experimental**
    * This Chatbot lets you experiment with different prompts using a local LLM
    * Interactions with Bot are monitoried, keep it work related and not private information
    * Do not share sensitive data with the bot
    * This bot will come and go as it is still in early development stages

    ## Bot Behavior
    * Bots and LLMs speak words that make sense, but are not necessarily true.
    * Bot currently has no access to any company internal knowledge base

    ## Example prompts: 
    * What are the top concerns for a network engineer in an insurance company?
    * You are a marketing content writer, help me make the following text more oriented for a seller to help them pitch this information to their customer. (Copy paste your text)

    """
    )
    return
