## This is our utilities library, will probably be renamed and split between Bot, Rag and other agents.
from libs import utilities

import default_config as cfg
import streamlit as st
from libs.streaming import StreamHandler

from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(
    page_title="OpenChat",
) 
st.header("OpenChat")


class ContextChatbot:
    def __init__(self):
        # self.openai_model = utilities.streamlit() # configure_openai()
        utilities.setup_streamlit() # configure_openai()

    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        # llm = ChatOpenAI(model_name=_self.openai_model, temperature=0, streaming=True)
        llm = ChatOllama(
            model="mistral",  # cfg.MODEL,temperature
            temperature=0,
            streaming=True,
        )
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain

    @utilities.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utilities.display_msg(user_query, "user")
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = chain.invoke({"input": user_query}, {"callbacks": [st_cb]})
                response = result["response"]
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
