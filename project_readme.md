# 🧠 ClipBrain AI

ClipBrain AI is an intelligent pipeline designed to process video and audio content (such as YouTube videos or recorded meetings) into structured, actionable insights. It acts as an automated assistant that not only transcribes and summarizes long-form media but also allows users to interactively chat with the video's content using Retrieval-Augmented Generation (RAG).

## 🚀 Features

* **Media Ingestion:** Automatically download audio from YouTube URLs or load local files.
* **AI Transcription:** Highly accurate speech-to-text processing using the Whisper AI model.
* **Contextual Analysis:** Generates smart titles, comprehensive summaries, and extracts structured data including:
  * ✅ Action Items
  * 🔑 Key Decisions
  * ❓ Open Questions
* **Interactive Chat (RAG):** Ask questions about the video content and get context-aware answers powered by Mistral AI.

## 🏗️ Architecture & Layers

The project is structured into distinct layers to separate the user interface from the heavy AI processing:

### Frontend (User Interface)
* **Streamlit Web GUI (`app.py`):** Provides a modern, responsive web application featuring custom CSS injections for styling (gradients, custom fonts, chat bubbles, and progress indicators). It uses an intuitive tabbed layout for Summaries, Analysis, Transcripts, and Chat.
* **CLI Entry (`main.py`):** A lightweight terminal alternative for quick, text-based processing and chatting without launching the web server.

### Backend (Core Processing Pipeline)
* **Audio Extraction (`utils/audio_extractor.py`):** Handles downloading media, format conversion (WAV 16kHz Mono), and chunking large audio files to prevent memory overload.
* **Transcription Engine (`utils/transcriber.py`):** Loads and runs the Whisper model to convert audio chunks into text.
* **LLM Analysis (`core/summarizer.py`, `core/extractor.py`):** Processes the raw transcript to generate a contextual title, a map-reduce summary, and extracts structured metadata.
* **RAG Engine (`core/rag.py`):** Builds a vector database of the transcript embeddings, enabling the LLM to answer user queries with high accuracy based solely on the video context.

## 🛠️ Technology Stack

* **Language:** Python
* **Frontend UI:** Streamlit
* **Audio Processing:** `yt-dlp` (YouTube extraction), `pydub` / `ffmpeg` (WAV conversion and chunking)
* **AI Transcription:** OpenAI Whisper
* **LLM & RAG:** Mistral AI, LangChain (LCEL)
* **Vector Store:** ChromaDB / FAISS (for embedding storage)
* **Environment:** `python-dotenv`

## 🧠 RAG Architecture (LangChain Expression Language - LCEL)

When chatting with your media, ClipBrain utilizes the following RAG workflow to fetch relevant context and generate accurate answers:

```text
                         USER QUESTION
                               │
                               ▼
                 ┌─────────────────────────┐
                 │        LCEL INPUT       │
                 └────────────┬────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
           RETRIEVER                RunnablePassthrough
                │                           │
                ▼                           │
       Relevant Documents                   │
                │                           │
                ▼                           │
      RunnableLambda(                       │
          format_docs                       │
      )                                     │
                │                           │
                ▼                           ▼
           "context"                   "question"
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                    ChatPromptTemplate
                              │
                              ▼
                         ChatMistralAI
                              │
                              ▼
                      StrOutputParser
                              │
                              ▼
                         FINAL ANSWER
```

## 💻 Usage

1. Clone the repository and install dependencies.
2. Set up your `.env` file with the required API keys (e.g., Mistral API key).
3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```
4. **Run the CLI:**
   ```bash
   python main.py
   ```