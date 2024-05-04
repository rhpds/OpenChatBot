
# LLM Configuration
## TODO: This should at some point be converted to YAML, making it easier to have more complex structures. 

MODEL = 'mistral'
#BASE_URL='http://192.168.1.171:11434'
BASE_URL='http://localhost:11434'
# Streamlit Headers
PAGE_TITLE="OpenChat"
SIDE_BAR_TEXT="""
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


# STREAMLIT_PAGE_TITLE = 'Ragnarok: Chat with **your** Data'
# STREAMLIT_BOT_TITLE = 'AAP2 Containerized Lab Bot :female-teacher:'
# STREAMLIT_SIDEBAR_TITLE = 'Add additional sources (PDFs)'

# USER_PROMPT = 'Ask questions about your lab, Ansible, and AAP2 Containerized:'
# USER_AVATAR = 'https://cloudassembler.com/images/avatar.png'
# # BOT_AVATAR = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Red_Hat_logo.svg/2560px-Red_Hat_logo.svg.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;"'
# BOT_AVATAR = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Red_Hat_logo.svg/2560px-Red_Hat_logo.svg.png'