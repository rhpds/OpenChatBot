#pip install pypdf
#pip install --upgrade --quiet  lark chromadb
#pip install langchain

from langchain.globals import set_debug
from langchain_community.llms import Ollama

## Development variables 

INPUT_DIR = "../../../../input_small/"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

debug=True

def metadata_func(record: dict) -> dict:
    """
    ## Creating Metadata to tag our documents (Chunks)
    In this piece, we are defining metadata information such as *Product* and *Document Type* from the actual file name of the document we are processing.
    This is pretty "Hard coded" and in the future we can get the LLM to provide a best guess about the *Product* and *Document Type*. 
    The function returns a metadata dictionary to be used when encoding the documents. 

    There is a cool code snippet here that we are not using, which will update the *source* metadata, for example, to add the URL of where the source will be available to the end user
```
    ## This is a good example of how one can modify the metadata, for example, to have correct URLs to the source documentation
    if "source" in metadata:
        source = metadata["source"].split("/")
        source = source[source.index("output"):]
        metadata["source"] = "/".join(source)
    print("record is:", record)
```
    """
    import re
    debug=0
    metadata={}
    # ## This is a good example of how one can modify the metadata, for example, to have correct URLs to the source documentation
    # if "source" in metadata:
    #     source = metadata["source"].split("/")
    #     source = source[source.index("output"):]
    #     metadata["source"] = "/".join(source)
    print("record is:", record) if debug else None
    print("processing for meta:", record.metadata['source']) if debug else None
    
    #TODO: Nothing, but if this was a real piece of code we would take these patterns and keywords into a config file and just loop over them. 
    
    regex_options_product = {
    "Ansible": re.compile(r"(ansible|automation)", re.IGNORECASE),
    "OpenShift": re.compile(r"(openshift|ocp|oap)", re.IGNORECASE),
    "RHEL": re.compile(r"(rhel|Red Hat Enterprise Linux)", re.IGNORECASE)
    }
    
    regex_options_doc_type = {
    "cheatsheet": re.compile(r"(cheatsheet|summary)", re.IGNORECASE),
    "objection": re.compile(r"(objection|handling)", re.IGNORECASE),
    "messaging": re.compile(r"(sales|play|playbook|value|messaging|message|framework)", re.IGNORECASE),
    "discovery": re.compile(r"(discovery|qualify|qualification)", re.IGNORECASE),
    "email": re.compile(r"(email)", re.IGNORECASE)
    
    }
    
    # Check each regex and execute different actions
    text = record.metadata['source']
    
    ## Add Product Meta data -> This will be replaced eventually with the LLM figuring this based on content, not filename
    print(text) if debug else None
    if regex_options_product["Ansible"].search(text):
        print("Ansible") if debug else None
        metadata['product'] = "Ansible"
    elif regex_options_product["OpenShift"].search(text):
        print("OpenShift") if debug else None
        metadata['product'] = "OpenShift"
    elif regex_options_product["RHEL"].search(text):
        print("RHEL") if debug else None
        metadata['product'] = "RHEL"
    else:
        print("Invalid option NO PRODUCT FOUND")

    if regex_options_doc_type["cheatsheet"].search(text):
        print("cheatsheet") if debug else None
        metadata['doc_type'] = "cheatsheet"
    elif regex_options_doc_type["objection"].search(text):
        print("objection") if debug else None
        metadata['doc_type'] = "objection"
    elif regex_options_doc_type["messaging"].search(text):
        print("messaging") if debug else None
        metadata['doc_type'] = "messaging"
    elif regex_options_doc_type["email"].search(text):
        print("email") if debug else None
        metadata['doc_type'] = "messaging"
    elif regex_options_doc_type["discovery"].search(text):
        print("discovery") if debug else None
        metadata['doc_type'] = "discovery"
    else:
        print("Invalid option NO PRODUCT FOUND")

    
    return metadata

def load_files(input_dir):
    """
    ## The Loader 
    Pretty simple stuff here:
    1. Provide directory where the source files are
    2. load them in with the appropriate "Loader", in this case: `PyPDFLoader
    3. The loader, in this case, will split each document by page, so if a document had 3 pages, this will create 3 documents 
    4. provide them to the next step as `loaded_documents`

    Note: Notice that we go from 15~ files, to 85~ Document Parts
    """
    from langchain_community.document_loaders import PyPDFLoader
    import os 
    import glob
    import time

    loaded_documents = []

    #input_dir=cfg.INPUT_DIR
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = input_dir + file
            print("Processsing:", pdf_path) if debug else None

            ## Should check here the file's Hash
            loader = PyPDFLoader(pdf_path) 
            file_data = loader.load()
            loaded_documents.extend(file_data)
            ## This code here is just to show case how the PDFs are being devided by page.
            for page in file_data:
                print("Page Metadata:", page.metadata)  if debug else None
    print("Passing",len(loaded_documents), "document parts")



    return loaded_documents

def split_files(loaded_documents):
    """
    ## Splitting and Embedding choices
    In this piece of code, we select our embedding, and more importantly:
    1. we are selectign the type of *splitter* we will use, in this case, we used `RecursiveCharacterTextSplitter` as a basic choice, there are possibly better choices we will need to expriment with
    2. We are selecting `chunk_size` and `chunk_overlap` defining how we cut down (chunk) the data before we embedd it into the VectorDB

    Note: Notice that we go from 85~ Document Parts, to 218~ document chunks
    """
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    ## TODO: This should be read from CONFIG
    chunk_size=1000
    chunk_overlap=200

    embeddings = OllamaEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_documents = text_splitter.split_documents(loaded_documents)

    # This kinda sucks, but it's the way i found to pass metadata before vectorDB phase, there is probably a better way
    for part in split_documents:
        part.metadata.update(metadata_func(part))
        print("part.metadata: ",part.metadata) if debug else None

    print("Passing",len(split_documents), "document chunks")

    return split_documents

def vector_files(split_documents):
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    """
    ## Putting our Documents (Chunks) into a VectorDB

    In this piece of code we are providing the document chunks to the VectorDB.
    In this case we are using `Chroma` as our Vector DB, there are many others like it. 

    TODO: For some reason, if you run this code over and over, Chrome will load the documents over and over that will create duplicates
    """


    if 'vectordb' not in globals():
        vectordb = {}

    vector_type="Chroma"
    vector_version="02"
    vector_db_name=vector_type + "_" + vector_version

    print(vector_db_name)

    vectordb[vector_db_name] = Chroma.from_documents(split_documents, embedding=OllamaEmbeddings(), persist_directory="./"+vector_db_name)
    vectordb[vector_db_name].persist()
    return vectordb[vector_db_name]




#For testing 


## Make new DB
#loaded_documents = load_files(INPUT_DIR)
#split_documents = split_files(loaded_documents)
#vectordb = vector_files(split_documents)

