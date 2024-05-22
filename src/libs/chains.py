import os

"""
In this file, we will have no mention of Chainlit or Streamlit

"""

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL", "http://localhost:11434"
)  # allows use of OLLAMA_BASE_URL="http://host.docker.internal:11434"


async def load_model(model):
    from langchain_community.chat_models import ChatOllama
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

    """
    Load## Function Name: `load_model`
    
    ### Description
    This function initializes and returns an instance of the `ChatOllama` model with specified settings. It prints the model loading step to standard output and configures the model for streaming operations with verbose output. The function is typically used to set up a language model for chat-based applications.
    
    ### Parameters
    - **model** (`str`): The name or identifier of the model configuration to be loaded. This parameter specifies which particular model variant of `ChatOllama` should be used.
    
    ### Returns
    - **llm** (`ChatOllama`): An instance of the `ChatOllama` class configured for verbose output and streaming, ready for chat operations.
    
    ### Example Usage
    ```python
    # Assuming the necessary classes and callbacks are already imported
    loaded_model = load_model('english_large')
    print("Model loaded and ready to use.")
    
    """
    print("loading module step:", model)
    llm = ChatOllama(
        model=model,
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url=OLLAMA_BASE_URL,
        streaming=True,
    )
    return llm


def memory_bot(model):
    from langchain.memory import ChatMessageHistory, ConversationBufferMemory
    from langchain.chains import ConversationChain

    """
    ## Function Name: `memory_bot`
    
    ### Description
    This function initializes and returns a `ConversationChain` that integrates a `ChatMessageHistory` for maintaining conversation context and a `ConversationBufferMemory` to manage the interactive memory of chat. It is designed to enhance chatbot responses by maintaining state across conversations. The function begins by initializing the bot and configuring memory management for the conversations.
    
    ### Parameters
    - **model** (`str`): The name or identifier of the model configuration to be used. This parameter specifies the model variant to load for the `ConversationChain`.
    
    ### Returns
    - **chain** (`ConversationChain`): A configured conversation chain that includes language model management and memory handling for enhanced conversation context.
    
    ### Example Usage
    ```python
    # Initialize the conversation chain for a memory-capable chatbot
    chat_chain = memory_bot('english_large')
    print("Chatbot is initialized with memory capabilities.")

    """
    print("memory_bot init")
    print("model:", model)
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="history",
        output_key="response",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationChain(
        llm=model,
        memory=memory,
    )
    return chain


def rag_bot(model, db_directory="./data/Sales_Rag"):
    """
    ## Function Name: `rag_bot`

    ### Description

    ### Parameters
    - **model** (`str`): The name or identifier of the model configuration to be used.
    - **db_directory**: The path to the vectorDB

    ### Returns
    - **chain**: The RAG chain returned

    ### Example Usage
    ```python
    # Initialize the RAG chain for chatbot
    chat_chain = rag_bot('mistral',db_directory="./data/Sales_Rag"))
    """
    ## TODO: db_directory is currently hard coded, this needs to be defined in settings.
    print("rag_bot init")
    vectordb = load_vectordb_from_disk(db_directory)
    # rag_chain = get_rag_chain_with_sources(vectordb)
    chain = get_rag_chain_with_sources(model, vectordb)

    return chain


def load_vectordb_from_disk(db_directory):
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    import os

    vectordb = Chroma(
        persist_directory=db_directory, embedding_function=OllamaEmbeddings()
    )
    # print("Debugging path problems:\n")
    # print(os.listdir(db_directory))

    # Debugging path problems
    # q="ansible stuff"
    # found_docs = vectordb.similarity_search(q,k=10)
    # print("Found docs:\n",found_docs)
    return vectordb


def self_query_retriver_chain(model, vectordb):
    from langchain_community.llms import Ollama
    from langchain.chains.query_constructor.base import AttributeInfo
    from langchain.retrievers.self_query.base import SelfQueryRetriever

    """
    ## Function Name: `load_vectordb_from_disk`

    ### Description
    This function initializes and returns an instance of the `Chroma` vector database configured with `OllamaEmbeddings`. It loads the vector store from a specified directory on disk, making it suitable for applications that require persistent, disk-based vector storage for embeddings.
    
    ### Parameters
    - **db_directory** (`str`): The directory path where the vector database is stored or will be stored. This parameter specifies the physical location on disk to persist vector data.
    
    ### Returns
    - **vectordb** (`Chroma`): An instance of the `Chroma` vector database using `OllamaEmbeddings` for embedding functionality. This vector store is ready for operations such as similarity searches and data retrieval.
    
    ### Example Usage
    ```python
    # Load the vector database from a specified directory
    vector_database = load_vectordb_from_disk('/path/to/database')
    print("Vector database loaded successfully.")

    """

    """
    ## Starting to define the self_Query retriever
    In the part, we define the `metadata_field_info`, it's an array that holds the definitions of the metadata that the self_query method will be looking. 
    Improving on the descriptions might yield better results.
    """
    metadata_field_info = [
        AttributeInfo(
            name="product",
            description="The Product discussed in the question. One of ['Ansible', 'OpenShift', 'RHEL']",
            type="string",
        ),
        AttributeInfo(
            name="doc_type",
            description="the sales topic discussed in the document. One of ['cheatsheet','objection','messaging','discovery','email']",
            type="string",
        ),
    ]

    """
    ## Self_Query retriever 
    """
    # set_debug(True)

    document_content_description = (
        "Sales materials of a software vendor usually describing a single product"
    )

    # llm = Ollama(model="mistral",temperature=0, verbose=True)
    llm = model
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectordb,
        document_content_description,
        metadata_field_info,
        #    verbose=True,
        #    use_original_query=True)
    )

    """
    ## Printing the result, documents and their content

    """
    # i=0
    # for i, doc in enumerate(retriever_result):
    #     print(f"{i + 1}.", doc.metadata)
    #     formatted_content = doc.page_content.replace('\n', ' ')  # Replace newline characters with space
    #     formatted_content = formatted_content.replace('. ', '.\n')  # Add a newline after each sentence for readability
    #     #print("Page Content:\n",formatted_content)
    # return retriever_result
    return retriever


def get_rag_chain_with_sources(model, vectordb):
    from langchain_core.output_parsers import StrOutputParser
    from langchain.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.runnables import RunnableParallel
    from langchain_community.chat_models import ChatOllama
    from langchain.globals import set_debug

    """
    ## Function Name: `get_rag_chain_with_sources`
    
    ### Description
    This function constructs and returns a Retrieve-and-Generate (RAG) chain that integrates a retriever model with a generator model to process queries. The chain uses a vector database (`vectordb`) for retrieving relevant documents as context, and an Ollama language model to generate responses based on the retrieved context. The setup includes custom templates for prompt formatting and parallel processing of context retrieval and question handling.
    
    ### Parameters
    - **vectordb** (`Chroma`): An instance of a vector database used for retrieving relevant documents based on query similarity. This database should be pre-populated with documents and their embeddings.
    
    ### Returns
    - **rag_chain_with_source** (`RunnableParallel`): A RAG chain that operates in parallel to handle context retrieval and response generation, structured to enhance the relevance and specificity of the generated answers.
    
    ### Example Usage
    ```python
    # Assuming the vector database and necessary imports are already configured
    vectordb = load_vectordb_from_disk('/path/to/vectordb')
    rag_chain = get_rag_chain_with_sources(vectordb)
    response = rag_chain.run({"question": "What are common objections in sales?"})
    print("Generated response:", response)

    """

    set_debug(True)

    template = """Answer the question based on the context provided, be brief and polite
    refer to the user as seller and start with a greeting
    <context>
    {context}
    </context>
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    # llm = Ollama(model="mistral")
    llm = model
    retriever = self_query_retriver_chain(model, vectordb)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # rag_chain = prompt| llm #| StrOutputParser()

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(response=rag_chain_from_docs)

    return rag_chain_with_source
