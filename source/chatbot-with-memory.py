# import utilities
from libs import utilities

import streamlit as st
from libs.streaming import StreamHandler

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="OpenChat", page_icon="⭐")
st.header("OpenChat")
st.write(
    "Chat with Open Source Mistral"
)  # Enhancing Chatbot Interactions through Context Awareness')
# st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/2_%E2%AD%90_context_aware_chatbot.py)')


class ContextChatbot:
    def __init__(self):
        self.openai_model = utilities.configure_openai()

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
