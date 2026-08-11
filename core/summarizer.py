

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from langchain_core.output_parsers import StrOutputParser
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]
from langchain_core.runnables import RunnableLambda

import os


def get_llm():
    model = ChatMistralAI(model = "mistral-small-latest", mistral_api_key = os.getenv("MISTRAL_API_KEY"), temperature = 0.3)
    return model

def split_transcript(transcript: str) -> list:
    print("splitting transcript into chunks.")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000, 
        chunk_overlap = 300
    )

    return splitter.split_text(transcript)

def chunks_summarizer(transcript:str)->str:
    chunks = split_transcript(transcript)

    print("Generating summary of each chunks independently.")

    chunk_summarize_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a video transcript concisely."),
        ("human", "{text}"),
    ])

    model = get_llm()

    chunk_summarize_pipeline = RunnableLambda(lambda x: {"text": x}) | chunk_summarize_prompt | model | StrOutputParser()

    chunks_summary = []
    for chunk in chunks:
        chunks_summary.append(chunk_summarize_pipeline.invoke(chunk))
    
    print("Joining the list of 'chunk of summaries'")
    summary = "\n\n".join(chunks_summary)

    return summary


def final_summary(transcript:str)->str:
    
    summary = chunks_summarizer(transcript)

    print("\n\nGenerating Final summmary.")

    summaries_summarize_prompt = ChatPromptTemplate.from_messages([
         (
            "system",
            "You are an expert video summarizer. Combine these partial summaries "
            "into one final professional video summary in bullet points.",
        ),
        ("human", "{summary}"),
    ])

    model = get_llm()

    final_pipeline = RunnableLambda(lambda x: {"summary": x}) | summaries_summarize_prompt | model | StrOutputParser()

    result = final_pipeline.invoke(summary)
    # print(f"FINAL SUMMARY: {result[:3000]}")
    return result



def generate_title(transcript: str) ->str:
    print("Generating Title.")

    title_prompt = ChatPromptTemplate.from_messages([
        ("system", "Based on the meeting transcript, generate a short professional meeting title (max 8 words). Only return the title, nothing else."),
        ("human", "{text}")
    ])

    model = get_llm()

    title_pipeline = RunnableLambda(lambda x: {"text" : x}) | title_prompt | model | StrOutputParser()

    title = title_pipeline.invoke(transcript[:2000])
    # print(f"TITLE: {title}")
    return title.strip()