from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
import os 
from langchain_mistralai import ChatMistralAI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from core.vector_store import build_vector_store, load_vector_store, retriever

#create llm
def get_llm():
    return ChatMistralAI(model = "mistral-small-latest",
        temperature=0.3,
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )

#convert retrived document into plain text
def format_docs(documents):
    return "\n\n".join( document.page_content for document in documents )


#create the prompt
def get_prompt():
    return ChatPromptTemplate.from_messages(
        [ ( "system", """You are an expert meeting assistant. 
            Answer the user's question using ONLY the meeting transcript provided in the context. 
            If the answer cannot be found in the context, say: "I could not find this information in the meeting transcript."
            Be concise and precise. Context: {context} """ ), 
        ( "human", "{question}" ), ]
        )

# build rag chain for new transcript 
def build_rag_chain(transcript:str):
    print("\n\n building rag chain.")
    vector_store = build_vector_store(transcript)
    retriever_response = retriever(vector_store)
    llm = get_llm()
    prompt = get_prompt()

    #rag chain
    chain = RunnableParallel({
            "context": retriever_response | format_docs,
            "question": RunnablePassthrough()
        }) | prompt | llm | StrOutputParser()

    return chain

# Load an existing vector store
def load_rag_chain(transcript:str):
    print("\n\n loading rag chain.")
    vector_store = load_vector_store()
    retriever_response = retriever(vector_store)
    llm = get_llm()
    prompt = get_prompt()

    # rag chain
    chain = RunnableParallel({
            "context" : retriever_response | format_docs,
            "question" : RunnablePassthrough()
        }) | prompt | llm | StrOutputParser()

    return chain

# ask question
def ask_questions(chain, question:str): 
    print(f"Question: {question}")
    answer = chain.invoke(question)
    # print(f"Answer: {answer}") 
    return answer