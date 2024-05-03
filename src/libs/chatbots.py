import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import default_config as cfg
from langchain.callbacks.base import BaseCallbackHandler
from .chains import *


### TODO:
# * See how StreamHandler can fit into ContextChatbot class
# * Class should have nothing hardcoded, or using default_config directly, values should be passed when creating the object in main.py 

### Development VARS
with_rag=True

class StreamHandler(BaseCallbackHandler):
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

class ContextChatbot:
    ## TODO: This fuction should not be here, it should be part of the overall APP code
    def setup_streamlit(self):
        """
        Function to setup streamlit titles etc configurations
        """

        ## TODO This should recieve values when called, not have them hard coded
        ## Does this function even belong here? is it part of the chatbot, or part of the overall wrapper?
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
    
    def __init__(self):
        self.setup_streamlit() 
    
    ## TODO: when this line is removed, the chatbot stops having memory, this should just cache, but, this might be another issue.
    """ in streamlit python library, what does st.cache_resource do? 
    In Streamlit Python library, st.cache_resource is a decorator used to cache the results of a function or a computation to improve the performance 
    of your application. When you apply this decorator to a function, Streamlit will store the result of that function in its cache and serve it from 
    there instead of re-computing it every time the same function is called with the same input. This can significantly reduce the amount of time 
    required to run your application, especially if the function involves expensive computations or I/O operations.
    """
    @st.cache_resource 
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        ## TODO: This should be set to receive model, base_url, and others when called, not use cfg file (or use it if nothing is provided)
        llm = ChatOllama(
            model=cfg.MODEL,  # cfg.MODEL,temperature
            base_url=cfg.BASE_URL,
            temperature=0,
            streaming=True,
        )
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    
    def setup_rag_chain(_self):
        ## This is the path, relative to where the python/streamlit was called
        db_directory = "./src/libs/loaders/Chroma_01"

        vectordb = load_vectordb_from_disk(db_directory)
        rag_chain = get_rag_chain_with_sources(vectordb)

        return rag_chain
    def main(self):
        
        user_query = st.chat_input(placeholder="Ask me anything!")
        if with_rag:
            chain = self.setup_rag_chain()
            if user_query:
                self.display_msg(user_query, "user")
                with st.chat_message("assistant"):
                    st_cb = StreamHandler(st.empty())
                    result = chain.invoke({"input": user_query}, {"callbacks": [st_cb]})
                    #result = chain.invoke(user_query)
                    response = result["response"]
                    print(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
        else:
            chain = self.setup_chain()
            if user_query:
                self.display_msg(user_query, "user")
                with st.chat_message("assistant"):
                    st_cb = StreamHandler(st.empty())
                    result = chain.invoke({"input": user_query}, {"callbacks": [st_cb]})
                    response = result["response"]
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )            
    ## TODO: Make variable the avatar part isn't working here, and should be defined in the config file
    def display_msg(self,msg, author):
        """Method to display message on the UI

        Args:
            msg (str): message to display
            author (str): author of the message -user/assistant
        """
        # this was previously a decorator, but I'm not sure it needs to be. could be wrong 
        self.enable_chat_history(self)
        st.session_state.messages.append(
            {
                "role": author,
                "content": msg,
                "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Red_Hat_logo.svg/2560px-Red_Hat_logo.svg.png"
                if author == "user"
                else "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Red_Hat_logo.svg/2560px-Red_Hat_logo.svg.png",
            }
        )
        st.chat_message(author).write(msg)
    def enable_chat_history(self,func):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])
