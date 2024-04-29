import os
import openai
import random
import streamlit as st
from datetime import datetime

#decorator
def enable_chat_history(func):
#    if os.environ.get("OPENAI_API_KEY"):

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

    avatar = "https://avatars.dicebear.com/api/avataaars/1.svg" if "user" == "user" else "https://avatars.dicebear.com/api/avataaars/2.svg"
    # to show chat history on ui
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
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
    st.session_state.messages.append({"role": author, "content": msg, "avatar": "https://avatars.dicebear.com/api/avataaars/1.svg" if author == "user" else "https://avatars.dicebear.com/api/avataaars/2.svg"})
    st.chat_message(author).write(msg)

def configure_openai():
    print("Configuring - old OpenAI Code")
    st.sidebar.title("Chatbot Configuration")
    st.sidebar.write("This Chatbot is powered by locally running Mistral")
    st.sidebar.write("\nWe can put whatever we like here")
    st.sidebar.write("...")
    st.sidebar.write("...")
    st.sidebar.write("...")
    """
    
    """

    # openai_api_key = st.sidebar.text_input(
    #     label="OpenAI API Key",
    #     type="password",
    #     value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
    #     placeholder="sk-..."
    #     )
    # if openai_api_key:
    if True:
        st.session_state['OPENAI_API_KEY'] = "foo"
        # st.session_state['OPENAI_API_KEY'] = openai_api_key
        # os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()
    print("## A level 2 title")
    model = "gpt-3.5-turbo"
    # try:
    #     client = openai.OpenAI()
    #     available_models = [{"id": i.id, "created":datetime.fromtimestamp(i.created)} for i in client.models.list() if str(i.id).startswith("gpt")]
    #     available_models = sorted(available_models, key=lambda x: x["created"])
    #     available_models = [i["id"] for i in available_models]

    #     model = st.sidebar.selectbox(
    #         label="Model",
    #         options=available_models,
    #         index=available_models.index(st.session_state['OPENAI_MODEL']) if 'OPENAI_MODEL' in st.session_state else 0
    #     )
    st.session_state['OPENAI_MODEL'] = model
    # except openai.AuthenticationError as e:
    #     st.error(e.body["message"])
    #     st.stop()
    # except Exception as e:
    #     print(e)
    #     st.error("Something went wrong. Please try again later.")
    #     st.stop()
    return model