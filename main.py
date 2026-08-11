from dotenv import load_dotenv
load_dotenv()
from utils.audio_extractor import process_input
from utils.transcriber import transcribe_all
from core.summarizer import final_summary, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag import build_rag_chain, ask_questions


def run_pipeline(source: str)-> list:
    audio_chunks = process_input(source)
    transcription = transcribe_all(audio_chunks)
    summary = final_summary(transcription)
    title = generate_title(transcription)
    actionable_items = extract_action_items(transcription)
    key_decisions = extract_key_decisions(transcription)
    questions = extract_questions(transcription)
    chain = build_rag_chain(transcription)

    return {
            "title": title,
            "transcript": transcription,
            "summary": summary,
            "action_items": actionable_items,
            "key_decisions": key_decisions,
            "open_questions": questions,
            "rag_chain": chain,
        }

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    # language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_questions(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")