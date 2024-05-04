from libs.chatbots import ContextChatbot
import default_config as cfg
import streamlit as st

def setup_streamlit(sidebar_title="sidebar title",sidebar_text="sidebar text"):
        """
        Function to setup streamlit titles etc configurations
        """
        st.set_page_config(page_title="OpenChat",)

        st.header("OpenChat")
        ## TODO This should recieve values when called, not have them hard coded
        ## Does this function even belong here? is it part of the chatbot, or part of the overall wrapper?
        st.sidebar.title(sidebar_title)
        st.sidebar.write(sidebar_text)
        return
setup_streamlit() 

if __name__ == "__main__":
    obj = ContextChatbot()

    obj.main()