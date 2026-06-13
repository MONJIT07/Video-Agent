import streamlit as st
import time
import re
from dotenv import load_dotenv

# ─── Page config must be FIRST ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ─── CSS Injection ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- Google Fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ---------- Root palette ---------- */
:root {
    --bg-dark:       #0d0f14;
    --bg-card:       #13161e;
    --bg-card-hover: #1a1e28;
    --accent:        #6c63ff;
    --accent-soft:   #8b83ff;
    --accent-glow:   rgba(108, 99, 255, 0.18);
    --teal:          #1de8b5;
    --amber:         #f5a623;
    --coral:         #ff6b6b;
    --text-primary:  #e8eaf0;
    --text-muted:    #7a82a0;
    --border:        rgba(255,255,255,0.08);
    --border-accent: rgba(108,99,255,0.4);
}

/* ---------- Global reset ---------- */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ---------- Hero banner ---------- */
.hero {
    background: linear-gradient(135deg, #0d0f14 0%, #1a1230 50%, #0d1220 100%);
    border: 1px solid var(--border-accent);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, var(--accent-glow), transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #fff 30%, var(--accent-soft));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .5rem 0;
}
.hero-sub {
    font-size: 1rem;
    color: var(--text-muted);
    margin: 0;
}

/* ---------- Glassy cards ---------- */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    transition: border-color .2s, background .2s;
}
.glass-card:hover { border-color: var(--border-accent); background: var(--bg-card-hover); }
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: .75rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--accent-soft);
    margin: 0 0 .8rem 0;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.card-title .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
    display: inline-block;
    box-shadow: 0 0 8px var(--accent);
}

/* ---------- Stat pills ---------- */
.stat-row { display: flex; gap: .8rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.stat-pill {
    background: #1a1e28;
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: .35rem 1rem;
    font-size: .82rem;
    color: var(--text-muted);
    display: inline-flex;
    align-items: center;
    gap: .4rem;
}
.stat-pill span { color: var(--text-primary); font-weight: 600; }

/* ---------- Progress bar ---------- */
.step-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1rem 0 1.6rem;
}
.step-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}
.step-item:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 14px; left: 60%;
    width: 80%; height: 2px;
    background: var(--border);
}
.step-item.done:not(:last-child)::after { background: var(--accent); }
.step-circle {
    width: 28px; height: 28px;
    border-radius: 50%;
    border: 2px solid var(--border);
    background: var(--bg-card);
    display: flex; align-items: center; justify-content: center;
    font-size: .7rem; font-weight: 700;
    color: var(--text-muted);
    position: relative; z-index: 1;
    transition: all .3s;
}
.step-item.done .step-circle {
    border-color: var(--accent);
    background: var(--accent-glow);
    color: var(--accent-soft);
    box-shadow: 0 0 10px var(--accent-glow);
}
.step-item.active .step-circle {
    border-color: var(--teal);
    background: rgba(29,232,181,.1);
    color: var(--teal);
    animation: pulse-ring 1.4s ease-in-out infinite;
}
.step-label {
    font-size: .67rem;
    margin-top: .4rem;
    color: var(--text-muted);
    text-align: center;
    white-space: nowrap;
}
.step-item.done .step-label { color: var(--accent-soft); }
.step-item.active .step-label { color: var(--teal); }

@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(29,232,181,.4); }
    70%  { box-shadow: 0 0 0 8px rgba(29,232,181,0); }
    100% { box-shadow: 0 0 0 0 rgba(29,232,181,0); }
}

/* ---------- Action items list ---------- */
.action-list { list-style: none; padding: 0; margin: 0; }
.action-list li {
    display: flex;
    align-items: flex-start;
    gap: .7rem;
    padding: .55rem 0;
    border-bottom: 1px solid var(--border);
    font-size: .9rem;
    line-height: 1.5;
    color: var(--text-primary);
}
.action-list li:last-child { border-bottom: none; }
.action-list .badge {
    min-width: 22px; height: 22px;
    border-radius: 6px;
    background: var(--accent-glow);
    color: var(--accent-soft);
    font-size: .7rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ---------- Chat bubble ---------- */
.chat-wrap { display: flex; flex-direction: column; gap: .9rem; }
.bubble {
    max-width: 82%;
    padding: .75rem 1.1rem;
    border-radius: 16px;
    font-size: .9rem;
    line-height: 1.6;
}
.bubble.user {
    align-self: flex-end;
    background: var(--accent-glow);
    border: 1px solid var(--border-accent);
    color: var(--text-primary);
    border-bottom-right-radius: 4px;
}
.bubble.ai {
    align-self: flex-start;
    background: var(--bg-card-hover);
    border: 1px solid var(--border);
    color: var(--text-primary);
    border-bottom-left-radius: 4px;
}
.bubble-label {
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .35rem;
    opacity: .6;
}

/* ---------- Input overrides ---------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-card-hover) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: .02em !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: scale(.97) !important; }

/* ---------- Spinner override ---------- */
.stSpinner { color: var(--teal) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2f3d; border-radius: 3px; }

/* ---------- Expandable section ---------- */
.stExpander { border: 1px solid var(--border) !important; border-radius: 12px !important; }
details summary { color: var(--text-primary) !important; }

/* ---------- Animated typing dots ---------- */
.typing-dots { display: inline-flex; gap: 4px; align-items: center; }
.typing-dots span {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--teal);
    animation: bounce-dot .9s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: .15s; }
.typing-dots span:nth-child(3) { animation-delay: .3s; }
@keyframes bounce-dot {
    0%, 60%, 100% { transform: translateY(0); opacity: .6; }
    30%            { transform: translateY(-6px); opacity: 1; }
}

/* ---------- Section divider ---------- */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
    margin: 1.5rem 0;
}

/* ---------- Transcript text ---------- */
.transcript-box {
    background: #0b0d12;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    font-family: 'Space Grotesk', monospace;
    font-size: .83rem;
    line-height: 1.7;
    color: #9ba3bc;
    max-height: 280px;
    overflow-y: auto;
}

/* ---------- Source badge ---------- */
.source-badge {
    display: inline-flex; align-items: center; gap: .4rem;
    padding: .3rem .85rem;
    border-radius: 20px;
    font-size: .78rem;
    font-weight: 600;
    border: 1px solid;
}
.badge-yt  { color: #ff4444; border-color: rgba(255,68,68,.3);  background: rgba(255,68,68,.08); }
.badge-file { color: var(--teal); border-color: rgba(29,232,181,.3); background: rgba(29,232,181,.08); }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────────────────
def _init():
    defaults = {
        "pipeline_result": None,
        "chat_history": [],
        "processing": False,
        "current_step": -1,
        "source": "",
        "language": "english",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ─── Helpers ───────────────────────────────────────────────────────────────────
def is_youtube(url: str) -> bool:
    return bool(re.match(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/", url.strip()))


def render_step_bar(current: int):
    steps = ["Download", "Transcribe", "Summarise", "Extract", "Index"]
    icons  = ["⬇", "✍", "📋", "🔍", "🗂"]
    html = '<div class="step-bar">'
    for i, (lbl, ico) in enumerate(zip(steps, icons)):
        cls = "done" if i < current else ("active" if i == current else "")
        html += f'''
        <div class="step-item {cls}">
            <div class="step-circle">{ico if i < current else (ico if i == current else str(i+1))}</div>
            <div class="step-label">{lbl}</div>
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def fmt_list(raw: str) -> str:
    """
    Render extractor output as a styled HTML list.
    Handles: numbered (1. / 1)), bullets (- / * / bullet), plain lines.
    """
    if not raw or not raw.strip():
        return '<p style="color:var(--text-muted);font-size:.88rem;">Nothing identified.</p>'

    lines = raw.strip().splitlines()
    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # strip leading "1. " "1) " "- " "• " "* " "– "
        line = re.sub(r"^(\d+[\.\)]\s*)", "", line)
        line = re.sub(r"^[-•*–]\s+", "", line)
        line = line.strip()
        if line:
            items.append(line)

    if not items:
        return '<p style="color:var(--text-muted);font-size:.88rem;">Nothing identified.</p>'

    rows = "".join(
        f'<li><span class="badge">{i+1}</span>{item}</li>'
        for i, item in enumerate(items)
    )
    return f'<ul class="action-list">{rows}</ul>'


def card(title: str, icon: str, body_html: str):
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title"><span class="dot"></span>{icon} {title}</div>
        {body_html}
    </div>""", unsafe_allow_html=True)


# ─── Pipeline Wrapper ──────────────────────────────────────────────────────────
def run_pipeline_ui(source: str, language: str, step_ph, msg_ph):
    from core.transcriber import transcribe_all
    from core.summarizer import summarize, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rage import build_rag_chain
    from utils.audio_processor import process_input

    def _step(n: int, msg: str):
        st.session_state.current_step = n
        with step_ph.container():
            render_step_bar(n)
        msg_ph.markdown(f"<p style='color:var(--text-muted);font-size:.88rem;'>{msg}</p>",
                        unsafe_allow_html=True)

    _step(0, "📥 Downloading & extracting audio…")
    chunks = process_input(source)

    _step(1, "✍️ Transcribing audio segments…")
    transcript = transcribe_all(chunks, language)

    _step(2, "📋 Generating title & summary…")
    title   = generate_title(transcript)
    summary = summarize(transcript)

    _step(3, "🔍 Extracting action items, decisions & questions…")
    action_items = extract_action_items(transcript)
    decisions    = extract_key_decisions(transcript)
    questions    = extract_questions(transcript)

    _step(4, "🗂 Building RAG index…")
    rag_chain = build_rag_chain(transcript)

    return {
        "title":        title,
        "transcript":   transcript,
        "summary":      summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain":    rag_chain,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 1.5rem;'>
        <div style='font-size:2.4rem;'>🎬</div>
        <div style='font-family:"Space Grotesk",sans-serif;font-size:1.1rem;font-weight:700;
                    color:#fff;margin-top:.4rem;'>AI Video Assistant</div>
        <div style='font-size:.78rem;color:#7a82a0;margin-top:.25rem;'>
            Transcribe · Summarise · Chat
        </div>
    </div>
    <hr style='border:none;border-top:1px solid rgba(255,255,255,.07);margin:0 0 1.4rem;'>
    """, unsafe_allow_html=True)

    source = st.text_input(
        "YouTube URL or local file path",
        placeholder="https://youtube.com/watch?v=… or /path/to/file.mp4",
        value=st.session_state.source,
        key="source_input",
    )

    language = st.selectbox(
        "Transcription language",
        ["english", "hinglish", "hindi", "auto"],
        index=["english","hinglish","hindi","auto"].index(st.session_state.language),
    )

    run_btn = st.button("▶ Analyse Video", use_container_width=True)

    if st.session_state.pipeline_result:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.pipeline_result = None
            st.session_state.chat_history    = []
            st.session_state.processing      = False
            st.session_state.current_step    = -1
            st.session_state.source          = ""
            st.session_state.language        = "english"
            st.rerun()

    # Info block
    st.markdown("""
    <div style='margin-top:2rem;padding:1rem;background:#0d0f14;border-radius:12px;
                border:1px solid rgba(255,255,255,.06);'>
        <div style='font-size:.72rem;font-weight:600;letter-spacing:.1em;
                    text-transform:uppercase;color:#6c63ff;margin-bottom:.6rem;'>
            Capabilities
        </div>
        <div style='font-size:.8rem;color:#7a82a0;line-height:1.8;'>
            ✦ YouTube & local video/audio<br>
            ✦ Whisper transcription<br>
            ✦ AI summarisation<br>
            ✦ Action items extraction<br>
            ✦ RAG-powered Q&amp;A
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════

# Hero
src_label = ""
if source:
    if is_youtube(source):
        src_label = '<span class="source-badge badge-yt">▶ YouTube</span>'
    else:
        src_label = '<span class="source-badge badge-file">📁 Local file</span>'

st.markdown(f"""
<div class="hero">
    <div class="hero-title">AI Video Assistant</div>
    <p class="hero-sub">Drop a YouTube link or a local video — get transcripts, summaries,
    action items, and a conversational AI that knows your content.</p>
    {'<div style="margin-top:1rem">' + src_label + '</div>' if src_label else ''}
</div>
""", unsafe_allow_html=True)


# ─── Handle "Run" ──────────────────────────────────────────────────────────────
if run_btn and source.strip():
    # Always wipe ALL previous results and chat so a new video starts fresh
    st.session_state.source          = source.strip()
    st.session_state.language        = language
    st.session_state.processing      = True
    st.session_state.pipeline_result = None
    st.session_state.chat_history    = []   # ← clears old-video chat completely
    st.session_state.current_step    = -1

if st.session_state.processing and not st.session_state.pipeline_result:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="dot"></span>⚙ Processing pipeline</div>',
                unsafe_allow_html=True)
    step_ph = st.empty()
    msg_ph  = st.empty()
    # Render initial empty bar ONLY inside the placeholder (no extra call below)
    with step_ph.container():
        render_step_bar(-1)

    try:
        result = run_pipeline_ui(
            st.session_state.source,
            st.session_state.language,
            step_ph, msg_ph,
        )
        st.session_state.pipeline_result = result
        st.session_state.processing = False
        msg_ph.markdown(
            "<p style='color:var(--teal);font-weight:600;'>✅ Analysis complete!</p>",
            unsafe_allow_html=True)
        time.sleep(.8)
        st.rerun()
    except Exception as exc:
        st.session_state.processing = False
        st.error(f"❌ Pipeline error: {exc}")
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Results ───────────────────────────────────────────────────────────────────
res = st.session_state.pipeline_result
if res:
    # ── Title + quick stats row
    word_count  = len(res["transcript"].split())
    char_count  = len(res["transcript"])
    action_n    = len([l for l in res["action_items"].splitlines() if l.strip()])
    decision_n  = len([l for l in res["key_decisions"].splitlines() if l.strip()])
    question_n  = len([l for l in res["open_questions"].splitlines() if l.strip()])

    st.markdown(f"""
    <div class="glass-card" style="border-color:rgba(108,99,255,.35);">
        <div class="card-title"><span class="dot"></span>📌 Meeting / Video Title</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.45rem;
                    font-weight:700;color:#fff;margin-bottom:1rem;">
            {res['title']}
        </div>
        <div class="stat-row">
            <div class="stat-pill">Words <span>{word_count:,}</span></div>
            <div class="stat-pill">Characters <span>{char_count:,}</span></div>
            <div class="stat-pill">Action items <span>{action_n}</span></div>
            <div class="stat-pill">Decisions <span>{decision_n}</span></div>
            <div class="stat-pill">Questions <span>{question_n}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs for the four insight panels
    tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript = st.tabs(
        ["📋 Summary", "✅ Action Items", "🔑 Key Decisions", "❓ Questions", "📝 Transcript"]
    )

    with tab_summary:
        card("Summary", "📋",
             f'<p style="font-size:.92rem;line-height:1.75;color:var(--text-primary);margin:0">'
             f'{res["summary"]}</p>')

    with tab_actions:
        card("Action Items", "✅", fmt_list(res["action_items"]))

    with tab_decisions:
        card("Key Decisions", "🔑", fmt_list(res["key_decisions"]))

    with tab_questions:
        card("Open Questions", "❓", fmt_list(res["open_questions"]))

    with tab_transcript:
        st.markdown(
            f'<div class="transcript-box">{res["transcript"]}</div>',
            unsafe_allow_html=True
        )
        st.download_button(
            "⬇ Download transcript",
            data=res["transcript"],
            file_name="transcript.txt",
            mime="text/plain",
        )

    # ── Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Chat section
    st.markdown("""
    <div class="card-title" style="margin-bottom:1rem;">
        <span class="dot"></span>💬 Chat with your video
    </div>
    """, unsafe_allow_html=True)

    # Render history
    if st.session_state.chat_history:
        bubbles = ""
        for msg in st.session_state.chat_history:
            role_cls = "user" if msg["role"] == "user" else "ai"
            label    = "You" if msg["role"] == "user" else "🤖 Assistant"
            bubbles += f"""
            <div class="bubble {role_cls}">
                <div class="bubble-label">{label}</div>
                {msg["content"]}
            </div>"""
        st.markdown(f'<div class="chat-wrap">{bubbles}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    # Input row
    col_q, col_btn = st.columns([5, 1])
    with col_q:
        question = st.text_input(
            "Ask anything about the video…",
            placeholder="e.g. What were the main decisions made?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_btn:
        ask_btn = st.button("Ask ↗", use_container_width=True)

    if ask_btn and question.strip():
        from core.rage import ask_question  # deferred import

        st.session_state.chat_history.append({"role": "user", "content": question.strip()})

        # Show typing indicator while getting answer
        typing_ph = st.empty()
        typing_ph.markdown("""
        <div class="bubble ai" style="margin-top:.6rem;">
            <div class="bubble-label">🤖 Assistant</div>
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>""", unsafe_allow_html=True)

        answer = ask_question(res["rag_chain"], question.strip())
        typing_ph.empty()

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    # Quick-prompt chips
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="margin-top:.8rem;display:flex;flex-wrap:wrap;gap:.5rem;">
            <span style="font-size:.75rem;color:var(--text-muted);align-self:center;">Try asking:</span>
        </div>""", unsafe_allow_html=True)
        chip_cols = st.columns(3)
        prompts = [
            "What are the main takeaways?",
            "Who are the key people mentioned?",
            "What follow-up tasks were assigned?",
        ]
        for col, prompt in zip(chip_cols, prompts):
            with col:
                if st.button(prompt, key=f"chip_{prompt[:10]}"):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    from core.rage import ask_question
                    answer = ask_question(res["rag_chain"], prompt)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()

# ─── Empty state ───────────────────────────────────────────────────────────────
elif not st.session_state.processing:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;color:#7a82a0;">
        <div style="font-size:4rem;margin-bottom:1rem;">🎬</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;
                    font-weight:600;color:#b0b8d0;margin-bottom:.6rem;">
            Ready to analyse your video
        </div>
        <div style="font-size:.9rem;max-width:400px;margin:0 auto;line-height:1.6;">
            Paste a YouTube URL or a local file path in the sidebar,
            choose your language, then hit <strong style="color:#6c63ff">Analyse Video</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)