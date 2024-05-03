from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st

class StreamHandler(BaseCallbackHandler):
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

def load_vectordb_from_disk(db_directory):
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    import os


    # Specify the directory where the database is stored
    

    # Load the ChromaDB instance from the specified directory
    vectordb = Chroma(persist_directory=db_directory, embedding_function=OllamaEmbeddings())
    print(os.listdir(db_directory))

    ## Debugging path problems
    # q="ansible stuff"
    # found_docs = vectordb.similarity_search(q,k=10)

    # print(found_docs)
    # import time

    # # Pause execution for 5 seconds
    # time.sleep(10)
    return vectordb

def self_query_retriver_chain(vectordb):
    from langchain_community.llms import Ollama
    """
    ## Starting to define the Self Query
    In the part, we define the `metadata_field_info`, it's an array that holds the definitions of the metadata that the self_query method will be looking. 
    Improving on the descriptions migth yield better results.
    """
    from langchain.chains.query_constructor.base import AttributeInfo
    from langchain.retrievers.self_query.base import SelfQueryRetriever

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
    #set_debug(True)

    document_content_description = "Sales materials of a software vendor usually describing a single product"


    llm = Ollama(model="mistral",temperature=0, verbose=True)
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectordb,
        document_content_description,
        metadata_field_info,
    #    verbose=True,
    #    use_original_query=True)
    )

    # ret_query = query + " return up to 10 documents"
    # retriever_result = retriever.invoke(ret_query)

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

def get_rag_chain_with_sources(vectordb):
    from langchain_community.llms import Ollama
    from langchain_core.output_parsers import StrOutputParser
    #from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser as StrOutputParser
    from langchain.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_core.runnables import RunnablePassthrough
    from langchain_community.chat_models import ChatOllama
    from langchain.globals import set_debug

    set_debug(True)
    template = """Answer the question based on the context provided, be brief and polite
    refer to the user as seller and start with a greeting
    if user is asking for objections, provide the objections AND the responses to the objection

    <context>
    {context}
    </context>
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    #llm = Ollama(model="mistral")
    llm = ChatOllama(
            model="mistral",  # cfg.MODEL,temperature
            base_url="http://192.168.1.171:11434",
            temperature=0,
            streaming=True,
        )
    retriever = self_query_retriver_chain(vectordb)
    print(retriever)
    #retriever=vectorstore.as_retriever()
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    #rag_chain = prompt| llm #| StrOutputParser()

    from langchain_core.runnables import RunnableParallel

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

## Query existing DB - For testing only

# input="What are OpenShift objections and their responses?"
# db_directory = "./loaders/Chroma_01"
# vectordb = load_vectordb_from_disk(db_directory)
# rag_chain = get_rag_chain_with_sources(vectordb)
# rag_answer= rag_chain.invoke(input)
# print(rag_answer)
