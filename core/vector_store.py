import os 
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "video_transcript"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"

def get_embeddings():
    print("inside get_embeddings function.")
    return HuggingFaceEmbeddings(model=EMBEDDING_MODEL, model_kwargs = {"device" : 'cpu'})

def build_vector_store(transcript: str)->Chroma:

    Splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    chunks = Splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={"index": i})
        for i, chunk in enumerate(chunks)
        ]

    embeddings = get_embeddings()
    print("\n building vector store.")
    vector_store = Chroma.from_documents(
        embedding=embeddings, 
        documents=docs, 
        collection_name=COLLECTION_NAME, 
        persist_directory=CHROMA_DIR
    )
    print("Vector store built completed.")
    return vector_store


def load_vector_store()->Chroma:
    print("\n\n\n loading vector store.")
    embeddings = get_embeddings()
    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    ) 

    return vector_store


def retriever(vector_store : Chroma, k : int = 4):
    print("\n\n retriver function.")
    retriever_response = vector_store.as_retriever(
        search_type='similarity',
        search_kwargs= {"k":k}
    )
    return retriever_response