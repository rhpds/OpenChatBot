## This is our utilities library, will probably be renamed and split between Bot, Rag and other agents.
#from libs import utilities
from libs.chatbots import ContextChatbot
import default_config as cfg
import streamlit as st
#from libs.streaming import StreamHandler

st.set_page_config(
    page_title="OpenChat",
) 
st.header("OpenChat")


if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
