from numba import boolean
import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None

def load_model():

    global _model

    if _model is None:
        print("\nloading whisper model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully.") 
    return _model

def transcribe_chunk(audio_chunk_path:str, translate: bool)->str:
    model = load_model()
    
    task = "translate" if translate else "transcribe"
    chunk_transcription = model.transcribe(
        audio_chunk_path, 
        task = task
        )
    return chunk_transcription['text']

def transcribe_all(audio_chunks:list, translate: bool=False)->str:
    
    chunks_transcription = ""
    for i, audio_chunk in enumerate(audio_chunks):
        chunk_transcription = transcribe_chunk(audio_chunk,translate)
        print(f"\n transcribing chunks {i+1}")
        chunks_transcription += chunk_transcription + " "
    
    print("\n\ntranscription completed.")
    # print(f"TRANSCRIPTION: {chunk_transcription[:3000]}")
    return chunks_transcription
