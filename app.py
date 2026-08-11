import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClipBrain AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1127 50%, #0a0f1e 100%);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1127 0%, #111827 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}

.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 50%, rgba(6,182,212,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(99,102,241,0.05) 0%, transparent 60%);
    animation: pulse-glow 4s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.hero-title {
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin: 0 0 0.5rem 0; line-height: 1.1;
}
.hero-subtitle { color: #94a3b8; font-size: 1.05rem; font-weight: 400; margin: 0; }

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px; padding: 1.8rem; margin-bottom: 1.5rem;
}

.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem;
    transition: border-color 0.3s ease, transform 0.2s ease;
}
.result-card:hover { border-color: rgba(99,102,241,0.4); transform: translateY(-2px); }
.result-card-title {
    font-size: 0.8rem; font-weight: 600; color: #6366f1;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;
}
.result-card-content { color: #cbd5e1; font-size: 0.95rem; line-height: 1.7; white-space: pre-wrap; }

.video-title-badge {
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.15));
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; text-align: center;
}
.video-title-text { font-size: 1.3rem; font-weight: 700; color: #e2e8f0; margin: 0; }

.chat-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    min-height: 200px; max-height: 450px; overflow-y: auto;
}
.chat-msg-user { display: flex; justify-content: flex-end; margin-bottom: 1rem; }
.chat-msg-user .bubble {
    background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white;
    border-radius: 18px 18px 4px 18px; padding: 0.75rem 1.1rem;
    max-width: 80%; font-size: 0.92rem; line-height: 1.5;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3);
}
.chat-msg-ai { display: flex; justify-content: flex-start; margin-bottom: 1rem; }
.chat-msg-ai .bubble {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(99,102,241,0.2);
    color: #cbd5e1; border-radius: 18px 18px 18px 4px; padding: 0.75rem 1.1rem;
    max-width: 80%; font-size: 0.92rem; line-height: 1.5;
}
.chat-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; flex-shrink: 0; margin: 0 0.5rem;
}
.avatar-ai { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.avatar-user { background: linear-gradient(135deg, #06b6d4, #3b82f6); }

.step-item {
    display: flex; align-items: flex-start; gap: 0.7rem;
    padding: 0.65rem 0.8rem; border-radius: 10px; margin-bottom: 0.4rem;
    transition: background 0.3s ease;
}
.step-item.pending { background: rgba(255,255,255,0.02); }
.step-item.running { background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); }
.step-item.done    { background: rgba(16,185,129,0.08);  border: 1px solid rgba(16,185,129,0.2); }
.step-item.error   { background: rgba(239,68,68,0.08);   border: 1px solid rgba(239,68,68,0.2); }
.step-icon { font-size: 1rem; line-height: 1; margin-top: 2px; flex-shrink: 0; }
.step-label { font-size: 0.82rem; color: #94a3b8; font-weight: 500; line-height: 1.3; }
.step-label.running { color: #a5b4fc; font-weight: 600; }
.step-label.done    { color: #6ee7b7; }
.step-label.error   { color: #fca5a5; }

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.25) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important; }

[data-testid="stTabs"] [role="tablist"] { gap: 0.3rem; border-bottom: 1px solid rgba(99,102,241,0.2) !important; }
[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important; color: #64748b !important;
    border-radius: 8px 8px 0 0 !important; padding: 0.5rem 1.2rem !important;
    font-weight: 500 !important; font-size: 0.88rem !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #a5b4fc !important; border-bottom: 2px solid #6366f1 !important;
    background: rgba(99,102,241,0.08) !important;
}
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ──────────────────────────────────────────────────────────────
def get_default_steps():
    return [
        {"label": "Download Audio from YouTube",       "status": "pending", "icon": "⬇️"},
        {"label": "Convert to WAV (16kHz Mono)",       "status": "pending", "icon": "🔄"},
        {"label": "Split into Audio Chunks",           "status": "pending", "icon": "✂️"},
        {"label": "Load Whisper Model",                "status": "pending", "icon": "🤫"},
        {"label": "Transcribe Audio Chunks",           "status": "pending", "icon": "📝"},
        {"label": "Generate Meeting Title",            "status": "pending", "icon": "🏷️"},
        {"label": "Summarise Transcript (Map-Reduce)", "status": "pending", "icon": "📋"},
        {"label": "Extract Action Items",              "status": "pending", "icon": "✅"},
        {"label": "Extract Key Decisions",             "status": "pending", "icon": "🔑"},
        {"label": "Extract Open Questions",            "status": "pending", "icon": "❓"},
        {"label": "Build Embedding Vector Store",      "status": "pending", "icon": "🗄️"},
        {"label": "Initialise RAG Chain (Mistral)",    "status": "pending", "icon": "🔗"},
    ]

defaults = {
    "pipeline_result": None,
    "chat_history": [],
    "rag_chain": None,
    "steps": get_default_steps(),
    "error_msg": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <span style="font-size:2.4rem;">🧠</span>
        <div style="font-size:1.3rem; font-weight:800;
                    background:linear-gradient(135deg,#6366f1,#8b5cf6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; margin-top:0.2rem;">ClipBrain AI</div>
        <div style="color:#64748b; font-size:0.75rem; margin-top:0.2rem;">
            YouTube &middot; Transcribe &middot; Analyse &middot; Chat
        </div>
    </div>
    <hr style="border-color:rgba(99,102,241,0.2); margin:0 0 1.2rem 0;">
    <div style="font-size:0.75rem; font-weight:700; color:#6366f1;
                text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
        Pipeline Steps
    </div>
    """, unsafe_allow_html=True)

    steps_placeholder = st.empty()

    def render_steps():
        icon_map = {"pending": "⬜", "running": "🔵", "done": "✅", "error": "❌"}
        html = ""
        for step in st.session_state.steps:
            s = step["status"]
            html += f"""
            <div class="step-item {s}">
                <span class="step-icon">{icon_map.get(s,'⬜')}</span>
                <span class="step-label {s}">{step['icon']} {step['label']}</span>
            </div>"""
        steps_placeholder.markdown(html, unsafe_allow_html=True)

    render_steps()

    st.markdown("""
    <hr style="border-color:rgba(99,102,241,0.2); margin:1.2rem 0;">
    <div style="font-size:0.72rem; color:#475569; line-height:2;">
        ⬜ Pending &nbsp; 🔵 Running<br>
        ✅ Done &nbsp;&nbsp;&nbsp; ❌ Error
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.pipeline_result:
        st.markdown("<hr style='border-color:rgba(99,102,241,0.2); margin:1.2rem 0;'>",
                    unsafe_allow_html=True)
        if st.button("🔄 Process New Video", use_container_width=True, key="reset_btn"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.session_state.steps = get_default_steps()
            st.rerun()

# ─── Step helper ────────────────────────────────────────────────────────────────
def set_step(idx, status):
    st.session_state.steps[idx]["status"] = status
    render_steps()

# ─── Pipeline ───────────────────────────────────────────────────────────────────
def run_pipeline(source: str):
    from utils.audio_extractor import download_youtube_audio, convert_to_wav, chunk_audio
    from utils.transcriber import load_model, transcribe_all
    from core.summarizer import final_summary, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rag import build_rag_chain

    set_step(0, "running")
    audio_mp3 = download_youtube_audio(source)
    set_step(0, "done")

    set_step(1, "running")
    audio_wav = convert_to_wav(audio_mp3)
    set_step(1, "done")

    set_step(2, "running")
    audio_chunks = chunk_audio(audio_wav, chunk_minutes=10)
    set_step(2, "done")

    set_step(3, "running")
    load_model()
    set_step(3, "done")

    set_step(4, "running")
    transcription = transcribe_all(audio_chunks)
    set_step(4, "done")

    set_step(5, "running")
    title = generate_title(transcription)
    set_step(5, "done")

    set_step(6, "running")
    summary = final_summary(transcription)
    set_step(6, "done")

    set_step(7, "running")
    action_items = extract_action_items(transcription)
    set_step(7, "done")

    set_step(8, "running")
    key_decisions = extract_key_decisions(transcription)
    set_step(8, "done")

    set_step(9, "running")
    questions = extract_questions(transcription)
    set_step(9, "done")

    set_step(10, "running")
    rag_chain = build_rag_chain(transcription)
    set_step(10, "done")

    set_step(11, "running")
    set_step(11, "done")

    return {
        "title": title,
        "transcript": transcription,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

# ─── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🧠 ClipBrain AI</h1>
    <p class="hero-subtitle">
        Paste any YouTube URL &rarr; ClipBrain downloads, transcribes, summarises,
        and lets you <strong style="color:#a5b4fc;">chat with any video</strong> using RAG.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────────────────────────────
if not st.session_state.pipeline_result:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.6rem;font-size:1.05rem;
                font-weight:700;color:#e2e8f0;margin-bottom:1rem;
                padding-bottom:0.6rem;border-bottom:1px solid rgba(99,102,241,0.2);">
        🎬 &nbsp; Enter Video Source
    </div>""", unsafe_allow_html=True)

    url_input = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="url_field",
    )

    col_btn, col_tip = st.columns([1, 3])
    with col_btn:
        process_btn = st.button("⚡ Process Video", use_container_width=True, key="process_btn")
    with col_tip:
        st.markdown("""
        <div style="color:#475569; font-size:0.82rem; padding-top:0.7rem;">
            💡 Processing takes a few minutes depending on video length.
            Watch the <strong style="color:#6366f1;">Pipeline Steps</strong> in the sidebar.
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.error_msg:
        st.error(f"❌  {st.session_state.error_msg}")

    if process_btn:
        if not url_input.strip():
            st.warning("⚠️ Please enter a valid YouTube URL.")
        else:
            st.session_state.steps = get_default_steps()
            st.session_state.error_msg = None
            render_steps()
            with st.spinner("🧠 ClipBrain is processing your video…"):
                try:
                    result = run_pipeline(url_input.strip())
                    st.session_state.pipeline_result = result
                    st.session_state.rag_chain = result["rag_chain"]
                    st.rerun()
                except Exception as e:
                    for i, step in enumerate(st.session_state.steps):
                        if step["status"] == "running":
                            set_step(i, "error")
                    st.session_state.error_msg = str(e)
                    st.rerun()

# ── Results ──────────────────────────────────────────────────────────────────────
else:
    result = st.session_state.pipeline_result

    st.markdown(f"""
    <div class="video-title-badge">
        <p class="video-title-text">📌 {result['title']}</p>
    </div>""", unsafe_allow_html=True)

    tab_summary, tab_analysis, tab_transcript, tab_chat = st.tabs([
        "📋  Summary", "🔍  Analysis", "📄  Transcript", "💬  Chat"
    ])

    with tab_summary:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-title">📋 Final Summary</div>
            <div class="result-card-content">{result['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with tab_analysis:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-card-title">✅ Action Items</div>
                <div class="result-card-content">{result['action_items']}</div>
            </div>
            <div class="result-card">
                <div class="result-card-title">❓ Open Questions</div>
                <div class="result-card-content">{result['open_questions']}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-card-title">🔑 Key Decisions</div>
                <div class="result-card-content">{result['key_decisions']}</div>
            </div>""", unsafe_allow_html=True)

    with tab_transcript:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-title">📄 Full Transcript</div>
            <div class="result-card-content">{result['transcript']}</div>
        </div>""", unsafe_allow_html=True)

    with tab_chat:
        st.markdown("""
        <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;">
            💬 Ask anything about the video. Answers are grounded in the transcript via RAG.
        </div>""", unsafe_allow_html=True)

        chat_html = '<div class="chat-container">'
        if not st.session_state.chat_history:
            chat_html += """<div style="text-align:center; color:#334155;
                            padding:3rem 0; font-size:0.9rem;">
                            🧠 Ask your first question about the video…</div>"""
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f"""
                    <div class="chat-msg-user">
                        <div class="bubble">{msg['content']}</div>
                        <div class="chat-avatar avatar-user">👤</div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div class="chat-msg-ai">
                        <div class="chat-avatar avatar-ai">🧠</div>
                        <div class="bubble">{msg['content']}</div>
                    </div>"""
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        q_col, btn_col = st.columns([5, 1])
        with q_col:
            user_question = st.text_input(
                "Your question",
                placeholder="e.g. What were the main decisions made?",
                label_visibility="collapsed",
                key="chat_input",
            )
        with btn_col:
            ask_btn = st.button("Ask ➤", use_container_width=True, key="ask_btn")

        if ask_btn and user_question.strip():
            from core.rag import ask_questions
            with st.spinner("🧠 Thinking…"):
                answer = ask_questions(st.session_state.rag_chain, user_question.strip())
            st.session_state.chat_history.append({"role": "user",  "content": user_question.strip()})
            st.session_state.chat_history.append({"role": "ai",    "content": answer})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
                st.session_state.chat_history = []
                st.rerun()
