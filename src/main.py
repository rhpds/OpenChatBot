from libs.chatbots import ContextChatbot
import default_config as cfg
import streamlit as st
st.set_page_config(
    page_title="OpenChat",
) 
st.header("OpenChat")

if __name__ == "__main__":
    obj = ContextChatbot()

    obj.main()