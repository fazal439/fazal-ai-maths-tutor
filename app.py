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
.hero-title::before,
.hero-title::after {
    content: none !important;
    display: none !important;
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
/* ===== PREMIUM DARK FLOATING THEME ===== */

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 174, 255, 0.18), transparent 28%),
        radial-gradient(circle at 85% 30%, rgba(128, 45, 255, 0.20), transparent 30%),
        linear-gradient(135deg, #020817 0%, #071a3d 48%, #090525 100%) !important;
    background-attachment: fixed !important;
}

[data-testid="stHeader"] {
    background: rgba(2, 8, 23, 0.96) !important;
    border-bottom: 1px solid rgba(63, 210, 255, 0.20);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020817 0%, #071738 55%, #12073b 100%) !important;
    border-right: 1px solid rgba(59, 215, 255, 0.30);
    box-shadow: 10px 0 35px rgba(0, 0, 0, 0.35);
}

/* Floating hero */
.hero {
    background: linear-gradient(
        135deg,
        rgba(10, 35, 90, 0.96),
        rgba(48, 25, 130, 0.92)
    ) !important;
    border: 1px solid rgba(80, 220, 255, 0.55) !important;
    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.45),
        0 0 35px rgba(54, 194, 255, 0.18) !important;
    animation: heroFloat 5s ease-in-out infinite !important;
    transition: all 0.35s ease !important;
}

.hero:hover {
    transform: translateY(-8px) scale(1.01) !important;
    box-shadow:
        0 28px 70px rgba(0, 0, 0, 0.55),
        0 0 45px rgba(77, 218, 255, 0.38) !important;
}

/* Floating feature cards */
.feature-card {
    border: 1px solid rgba(111, 225, 255, 0.45) !important;
    box-shadow:
        0 18px 38px rgba(0, 0, 0, 0.42),
        inset 0 1px 0 rgba(255, 255, 255, 0.16) !important;
    animation: cardFloat 4.5s ease-in-out infinite !important;
    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease,
        filter 0.35s ease !important;
}

.feature-card:nth-child(2) {
    animation-delay: 0.6s !important;
}

.feature-card:nth-child(3) {
    animation-delay: 1.2s !important;
}

.feature-card:hover {
    transform: translateY(-15px) scale(1.035) !important;
    filter: brightness(1.16) saturate(1.12) !important;
    box-shadow:
        0 28px 65px rgba(0, 0, 0, 0.55),
        0 0 35px rgba(79, 222, 255, 0.50) !important;
}

/* Chat messages floating glass effect */
[data-testid="stChatMessage"] {
    background: linear-gradient(
        135deg,
        rgba(7, 27, 69, 0.92),
        rgba(33, 32, 105, 0.88)
    ) !important;
    border: 1px solid rgba(72, 198, 255, 0.38) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

[data-testid="stChatMessage"]:hover {
    transform: translateY(-5px) !important;
    box-shadow:
        0 20px 45px rgba(0, 0, 0, 0.48),
        0 0 24px rgba(64, 205, 255, 0.24) !important;
}

/* Interactive buttons */
.stButton > button {
    background: linear-gradient(135deg, #075bd8, #5421b8) !important;
    color: white !important;
    border: 1px solid rgba(100, 224, 255, 0.65) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.32) !important;
    transition: all 0.28s ease !important;
}

.stButton > button:hover {
    transform: translateY(-5px) scale(1.04) !important;
    background: linear-gradient(135deg, #008cff, #7a24e8) !important;
    box-shadow:
        0 15px 32px rgba(0, 0, 0, 0.48),
        0 0 22px rgba(62, 213, 255, 0.55) !important;
}

/* Glowing question input */
[data-testid="stChatInput"] {
    background: rgba(4, 16, 44, 0.97) !important;
    border: 1px solid rgba(72, 211, 255, 0.70) !important;
    border-radius: 18px !important;
    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.48),
        0 0 24px rgba(61, 204, 255, 0.20) !important;
}

/* Floating animations */
@keyframes heroFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-8px);
    }
}

@keyframes cardFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}
/* Animated glowing profile circle */
.hero-title img {
    border: 3px solid #67e8f9 !important;
    border-radius: 50% !important;
    animation: profileGlow 2.2s ease-in-out infinite !important;
}

@keyframes profileGlow {
    0%, 100% {
        transform: scale(1);
        border-color: #67e8f9;
        box-shadow:
            0 0 8px #22d3ee,
            0 0 18px rgba(34, 211, 238, 0.55),
            0 0 28px rgba(124, 58, 237, 0.30);
    }

    50% {
        transform: scale(1.06);
        border-color: #c084fc;
        box-shadow:
            0 0 15px #22d3ee,
            0 0 35px rgba(34, 211, 238, 0.90),
            0 0 58px rgba(168, 85, 247, 0.75);
    }
}
/* Floating mathematics symbols */
.stApp::before,
.stApp::after {
    position: fixed;
    pointer-events: none;
    z-index: 0;
    color: rgba(103, 232, 249, 0.16);
    text-shadow: 0 0 18px rgba(34, 211, 238, 0.45);
    font-weight: bold;
}

.stApp::before {
    content: "π   ∑   √x   ∞";
    top: 18%;
    left: 24%;
    font-size: 42px;
    word-spacing: 150px;
    animation: mathFloatOne 12s ease-in-out infinite;
}

.stApp::after {
    content: "x²   ∫   Δ   a²+b²=c²";
    top: 65%;
    left: 35%;
    font-size: 30px;
    word-spacing: 120px;
    color: rgba(192, 132, 252, 0.14);
    text-shadow: 0 0 18px rgba(168, 85, 247, 0.45);
    animation: mathFloatTwo 15s ease-in-out infinite;
}

[data-testid="stAppViewContainer"] .main {
    position: relative;
    z-index: 1;
}

@keyframes mathFloatOne {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
        opacity: 0.25;
    }
    50% {
        transform: translate(35px, -28px) rotate(5deg);
        opacity: 0.65;
    }
}

@keyframes mathFloatTwo {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
        opacity: 0.20;
    }
    50% {
        transform: translate(-40px, 30px) rotate(-4deg);
        opacity: 0.55;
    }
}
/* Animated gradient title */
.hero-title .hero-title {
    background: linear-gradient(
        90deg,
        #67e8f9,
        #ffffff,
        #60a5fa,
        #c084fc,
        #67e8f9
    ) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    animation: titleLight 4s linear infinite !important;
    filter: drop-shadow(0 0 10px rgba(103, 232, 249, 0.45));
}

@keyframes titleLight {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 300% 50%;
    }
}
/* 3D interactive card tilt */
.feature-card {
    transform-style: preserve-3d !important;
    perspective: 1000px !important;
    cursor: pointer !important;
}

.feature-card:hover {
    transform:
        perspective(1000px)
        rotateX(-5deg)
        rotateY(6deg)
        translateY(-16px)
        scale(1.035) !important;
}

.feature-card:hover h3,
.feature-card:hover p,
.feature-card:hover .card-icon {
    transform: translateZ(28px) !important;
    transition: transform 0.35s ease !important;
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
import base64

with open("fazal_profile.jpg.jpeg", "rb") as image_file:
    profile_image = base64.b64encode(image_file.read()).decode()
st.markdown(
    '<div class="hero">'
    '<span class="math-symbol symbol1">π</span>'
f'<div class="hero-title" style="display:flex;align-items:center;gap:16px;"><img src="data:image/jpeg;base64,{profile_image}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #67e8f9;box-shadow:0 0 22px rgba(103,232,249,0.7);flex-shrink:0;">Fazal AI Maths Tutor</div>'    '<span class="math-symbol symbol3">Σ</span>'
    '<span class="math-symbol symbol4">∞</span>'
    
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

quick_question = None
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧮 Solve Equation", use_container_width=True):
        quick_question = "Solve 3x + 5 = 20 step by step."

with col2:
    if st.button("👦 Explain Simply", use_container_width=True):
        quick_question = "Explain fractions in very simple words."

with col3:
    if st.button("📝 Create Quiz", use_container_width=True):
        quick_question = "Create five mathematics practice questions."

typed_question = st.chat_input("Example: Solve 2x + 5 = 15")
question = typed_question or quick_question

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)
    conversation_context = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in st.session_state.messages[-8:]
    )
    tutor_prompt = f"""
You are Fazal AI Maths Tutor, a friendly and accurate mathematics teacher.

Current learning mode: {st.session_state.mode}
Previous conversation:
{conversation_context}

Follow-up instructions:
- Use the previous conversation to understand follow-up questions.
- If the student is confused, identify the exact confusing step.
- Explain that step again using simpler words and a clear sequence.
- Give a small example when helpful.
- Do not repeat the complete answer unless the student requests it.

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
                    model="gemini-3.5-flash-lite",
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