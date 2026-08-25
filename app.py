import streamlit as st
import time
from google import genai
st.set_page_config(
    page_title="Fazal AI Maths Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.markdown("""
<style>

/* Mobile responsive design */
@media screen and (max-width: 768px) {

    .block-container {
        max-width: 100% !important;
        padding: 1rem 0.8rem 6rem 0.8rem !important;
    }

    .hero {
        padding: 24px 18px !important;
        border-radius: 18px !important;
        text-align: center;
    }

    .hero-title {
        font-size: 28px !important;
        line-height: 1.2 !important;
        width: 100% !important;
    }

    .animated-statement {
        width: 100% !important;
        white-space: normal !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        border-right: none !important;
        animation: mobileFade 1.5s ease !important;
    }

    @keyframes mobileFade {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .math-symbol {
        font-size: 22px !important;
        opacity: 0.12 !important;
    }

    .status-box {
        padding: 13px !important;
        font-size: 13px !important;
        margin: 16px 0 !important;
    }

    /* Put every feature card on its own row */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 15px !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    .feature-card {
        width: 100% !important;
        min-height: 155px !important;
        box-sizing: border-box !important;
        margin-bottom: 5px !important;
        padding: 20px !important;
    }

    .feature-card h3 {
        font-size: 21px !important;
    }

    .feature-card p {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    .feature-icon {
        font-size: 34px !important;
    }

    .chat-heading {
        font-size: 21px !important;
        margin-top: 18px !important;
    }

    [data-testid="stChatMessage"] {
        font-size: 15px !important;
        padding: 10px !important;
    }

    [data-testid="stChatInput"] {
        width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Make all chat text clear and bright */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] span {
    color: #ffffff !important;
}

[data-testid="stChatMessage"] {
    font-size: 17px !important;
    line-height: 1.7 !important;
}

[data-testid="stChatMessage"] strong {
    color: #67e8f9 !important;
}

[data-testid="stChatMessage"] .katex {
    color: #fef08a !important;
}

[data-testid="stChatMessage"] code {
    color: #fef08a !important;
    background: #0f172a !important;
    padding: 3px 7px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Complete dark animated background */
.stApp {
    color: white;
    background:
        radial-gradient(circle at 15% 20%, #123b75 0%, transparent 30%),
        radial-gradient(circle at 85% 25%, #581c87 0%, transparent 32%),
        radial-gradient(circle at 70% 85%, #075985 0%, transparent 30%),
        linear-gradient(-45deg, #020617, #071a3d, #172554, #0f172a);
    background-size: 180% 180%;
    animation: backgroundMove 12s ease infinite;
}

@keyframes backgroundMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    max-width: 1150px;
    padding-top: 1.3rem;
}

/* Animated glowing hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 42px;
    border-radius: 28px;
    background: linear-gradient(
        120deg,
        rgba(29, 78, 216, 0.95),
        rgba(88, 28, 135, 0.95),
        rgba(8, 145, 178, 0.95)
    );
    background-size: 300% 300%;
    animation: heroColors 7s ease infinite, heroEntry 1s ease;
    box-shadow:
        0 0 30px rgba(59, 130, 246, 0.35),
        0 0 70px rgba(139, 92, 246, 0.22);
    border: 1px solid rgba(125, 211, 252, 0.45);
}

@keyframes heroColors {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes heroEntry {
    from {
        opacity: 0;
        transform: scale(0.90);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Animated title */
.hero-title {
    font-size: 46px;
    font-weight: 800;
    margin: 0;
    width: fit-content;
    background: linear-gradient(90deg, #ffffff, #67e8f9, #c4b5fd, #ffffff);
    background-size: 250%;
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    animation: titleShine 4s linear infinite, titleFloat 3s ease-in-out infinite;
}

@keyframes titleShine {
    from { background-position: 0%; }
    to { background-position: 250%; }
}

@keyframes titleFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
}

/* Animated statement */
.animated-statement {
    margin-top: 17px;
    font-size: 19px;
    font-weight: 500;
    color: #e0f2fe;
    overflow: hidden;
    white-space: nowrap;
    width: 0;
    border-right: 3px solid #67e8f9;
    animation:
        typing 5s steps(65, end) forwards,
        cursorBlink 0.7s infinite;
}

@keyframes typing {
    from { width: 0; }
    to { width: 78%; }
}

@keyframes cursorBlink {
    50% { border-color: transparent; }
}

/* Floating mathematics symbols */
.math-symbol {
    position: absolute;
    font-weight: bold;
    color: rgba(255,255,255,0.20);
    animation: symbolMovement 5s ease-in-out infinite;
}

.symbol1 {
    top: 18px;
    right: 50px;
    font-size: 43px;
}

.symbol2 {
    bottom: 15px;
    right: 150px;
    font-size: 35px;
    animation-delay: 1s;
}

.symbol3 {
    top: 18px;
    right: 260px;
    font-size: 37px;
    animation-delay: 2s;
}

.symbol4 {
    bottom: 15px;
    right: 340px;
    font-size: 33px;
    animation-delay: 3s;
}

@keyframes symbolMovement {
    0%, 100% {
        transform: translateY(0) rotate(0deg) scale(1);
    }
    50% {
        transform: translateY(-18px) rotate(15deg) scale(1.2);
    }
}

/* AI status */
.status-box {
    padding: 16px 21px;
    margin: 24px 0;
    border-radius: 16px;
    color: #cffafe;
    background: linear-gradient(
        90deg,
        rgba(6, 78, 59, 0.85),
        rgba(8, 145, 178, 0.70),
        rgba(30, 64, 175, 0.75)
    );
    background-size: 250%;
    border: 1px solid #22d3ee;
    animation: statusColors 5s linear infinite;
    box-shadow: 0 0 24px rgba(34, 211, 238, 0.20);
}

@keyframes statusColors {
    from { background-position: 0%; }
    to { background-position: 250%; }
}

.pulse {
    display: inline-block;
    width: 12px;
    height: 12px;
    margin-right: 10px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulseEffect 1.4s infinite;
}

@keyframes pulseEffect {
    0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.9); }
    70% { box-shadow: 0 0 0 13px rgba(34,197,94,0); }
    100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}

/* Colourful feature cards */
.feature-card {
    position: relative;
    overflow: hidden;
    min-height: 190px;
    padding: 25px;
    color: white;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.25);
    transition: 0.4s;
}

.card-one {
    background: linear-gradient(145deg, #1e3a8a, #0369a1, #0891b2);
    animation: cardOneMove 4s ease-in-out infinite;
    box-shadow: 0 15px 35px rgba(8,145,178,0.25);
}

.card-two {
    background: linear-gradient(145deg, #312e81, #6d28d9, #9333ea);
    animation: cardTwoMove 4.5s ease-in-out infinite;
    box-shadow: 0 15px 35px rgba(147,51,234,0.25);
}

.card-three {
    background: linear-gradient(145deg, #064e3b, #047857, #0891b2);
    animation: cardThreeMove 5s ease-in-out infinite;
    box-shadow: 0 15px 35px rgba(16,185,129,0.23);
}

@keyframes cardOneMove {
    0%, 100% { transform: translateY(0) rotate(0); }
    50% { transform: translateY(-10px) rotate(-1deg); }
}

@keyframes cardTwoMove {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.035); }
}

@keyframes cardThreeMove {
    0%, 100% { transform: translateY(0) rotate(0); }
    50% { transform: translateY(-10px) rotate(1deg); }
}

.feature-card:hover {
    transform: translateY(-14px) scale(1.05);
    border-color: #ffffff;
    filter: brightness(1.15);
}

.feature-card h3 {
    color: white;
    font-size: 24px;
    margin: 9px 0;
}

.feature-card p {
    color: #e0f2fe;
    line-height: 1.6;
}

.feature-icon {
    display: inline-block;
    font-size: 43px;
    animation: iconMovement 2s ease-in-out infinite;
}

@keyframes iconMovement {
    0%, 100% { transform: scale(1) rotate(-5deg); }
    50% { transform: scale(1.25) rotate(8deg); }
}

/* Moving shine over cards */
.feature-card::after {
    content: "";
    position: absolute;
    top: -100%;
    left: -70%;
    width: 50%;
    height: 300%;
    background: rgba(255,255,255,0.13);
    transform: rotate(30deg);
    animation: cardShine 4s infinite;
}

@keyframes cardShine {
    0% { left: -70%; }
    60%, 100% { left: 140%; }
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #020617, #0f2862, #312e81);
    border-right: 1px solid rgba(96,165,250,0.35);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: white;
}

[data-testid="stSidebar"] .stButton button {
    color: #e0f2fe;
    background: linear-gradient(
        90deg,
        rgba(30,64,175,0.60),
        rgba(88,28,135,0.55)
    );
    border: 1px solid rgba(125,211,252,0.45);
    transition: 0.3s;
}

[data-testid="stSidebar"] .stButton button:hover {
    color: white;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    transform: translateX(8px) scale(1.03);
    box-shadow: 0 0 18px rgba(96,165,250,0.45);
}

/* Chat heading */
.chat-heading {
    color: white;
    font-size: 27px;
    margin-top: 24px;
    text-shadow: 0 0 16px rgba(56,189,248,0.40);
}

/* Chat messages */
.stChatMessage {
    color: white;
    border-radius: 19px;
    background: linear-gradient(
        120deg,
        rgba(15, 23, 42, 0.92),
        rgba(30, 58, 138, 0.72)
    );
    border: 1px solid rgba(96,165,250,0.45);
    animation: messageEntry 0.6s ease;
}

@keyframes messageEntry {
    from {
        opacity: 0;
        transform: translateX(-25px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Dark chat input */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #0f172a, #172554);
    border: 1px solid #3b82f6;
    border-radius: 17px;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}
/* Question input text */
[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    caret-color: #000000 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #475569 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "General Tutor"

with st.sidebar:
    st.title("🎓 Fazal AI")
    st.caption("Intelligent Mathematics Assistant")
    st.divider()

    if st.button("💬 New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("👦 Explain Like a Kid"):
        st.session_state.mode = "Explain Like a Kid"

    if st.button("📝 Practice Questions"):
        st.session_state.mode = "Practice Questions"

    if st.button("✅ Check My Answer"):
        st.session_state.mode = "Check My Answer"

    st.divider()
    st.write("🟢 AI Tutor: Ready")
    st.write("📚 Subject: Mathematics")
    st.write("🌐 Available Online")

st.markdown(
    '<div class="hero">'
    '<span class="math-symbol symbol1">π</span>'
    '<span class="math-symbol symbol2">√x</span>'
    '<span class="math-symbol symbol3">Σ</span>'
    '<span class="math-symbol symbol4">∞</span>'
    '<div class="hero-title">🎓 Fazal AI Maths Tutor</div>'
    '<div class="animated-statement">'
    'Your intelligent partner for learning mathematics step by step.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="status-box">
        <span class="pulse"></span>
        AI is active — Current learning mode:
        <b>{st.session_state.mode}</b>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card card-one">
        <span class="feature-icon">👦</span>
        <h3>Explain Simply</h3>
        <p>Learn difficult mathematics with simple language and clear steps.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card card-two">
        <span class="feature-icon">📝</span>
        <h3>Smart Practice</h3>
        <p>Generate personalised practice questions for every mathematics topic.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card card-three">
        <span class="feature-icon">✅</span>
        <h3>Check Answers</h3>
        <p>Submit your solution and receive immediate, helpful feedback.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="chat-heading">💬 Ask Your Mathematics Question</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Example: Solve 2x + 5 = 15")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    tutor_prompt = f"""
You are Fazal AI Maths Tutor, a friendly and accurate mathematics teacher.

Current learning mode: {st.session_state.mode}

Student's question:
{question}

Instructions:
- Answer only educational and mathematics-related questions.
- Explain the solution step by step.
- Use simple and clear English.
- Show formulas neatly.
- Check calculations carefully.
- If the mode is "Explain Like a Kid", use very easy language and a simple example.
- If the mode is "Practice Questions", create five practice questions and provide answers separately.
- If the mode is "Check My Answer", check the student's working and politely explain any mistake.
- Do not give an unnecessarily long answer.
"""

    with st.chat_message("assistant"):
        with st.spinner("Fazal AI is solving your question..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=tutor_prompt
                )

                answer = response.text

            except Exception as error:
    error_text = str(error)

    if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
        answer = (
            "⏳ The free AI service is currently busy. "
            "Please wait 30 seconds and try again."
        )
    else:
        answer = (
            "⚠️ The AI service is temporarily unavailable. "
            "Please try again shortly."
        )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })