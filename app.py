import streamlit as st
from agent import english_learning_agent
from memory import (
    init_db,
    save_learner,
    get_session_count,
    get_last_mode,
    get_recent_sessions
)

init_db()

st.set_page_config(
    page_title="English Learning Agent",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f7f9fc 0%, #eef3ff 100%);
}
.main-card {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #1f2a44;
}
.hero-subtitle {
    font-size: 18px;
    color: #5f6f89;
}
.feature-box {
    background: #f8fbff;
    border: 1px solid #dbe7ff;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    color: #1f2a44;
    font-weight: 600;
}
.metric-card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e1e8ff;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}
.metric-label {
    color: #6b7280;
    font-size: 14px;
}
.metric-value {
    color: #1f2a44;
    font-size: 24px;
    font-weight: 800;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    background-color: #315efb;
    color: white;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("👤 Learner Profile")

name = st.sidebar.text_input("Name", value="Hanan")

level = st.sidebar.selectbox(
    "Current English Level",
    ["I don't know", "A1", "A2", "B1", "B2", "C1", "C2"]
)

goal = st.sidebar.selectbox(
    "Learning Goal",
    [
        "Job interviews",
        "Workplace communication",
        "Technical English",
        "Daily conversation",
        "Project presentation"
    ]
)

mode = st.sidebar.selectbox(
    "Practice Mode",
    [
        "Level Assessment",
        "Conversation Practice",
        "Grammar Feedback",
        "Job Interview Role-play",
        "Daily Task",
        "Progress Summary"
    ]
)

if st.sidebar.button("Save Learner Profile"):
    save_learner(name, level, goal)
    st.sidebar.success("Profile saved successfully!")

st.markdown("""
<div class="main-card">
    <div class="hero-title">📚 English Learning Agent</div>
    <div class="hero-subtitle">
        A personalized AI English coach for Saudi tech learners — powered by Agent, Memory, RAG, Feedback, and Role-play.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="feature-box">🧠 AI Agent</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-box">📚 RAG Knowledge</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-box">💾 Learner Memory</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="feature-box">🎤 Role-play</div>', unsafe_allow_html=True)

st.markdown("### 📊 Learner Dashboard")

session_count = get_session_count(name)
last_mode = get_last_mode(name)

d1, d2, d3, d4 = st.columns(4)

with d1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sessions Completed</div>
        <div class="metric-value">{session_count}</div>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Current Level</div>
        <div class="metric-value">{level}</div>
    </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Learning Goal</div>
        <div class="metric-value">{goal}</div>
    </div>
    """, unsafe_allow_html=True)

with d4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Last Mode</div>
        <div class="metric-value">{last_mode}</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🕘 Recent Practice Sessions"):
    recent_sessions = get_recent_sessions(name)

    if recent_sessions:
        for session_mode, user_message, created_at in recent_sessions:
            st.write(f"**{session_mode}** — {user_message}")
            st.caption(created_at)
    else:
        st.write("No sessions yet.")

st.markdown("### 💬 Practice Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Write your English message here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Your English coach is thinking..."):
            response = english_learning_agent(
                user_message=user_input,
                learner_name=name,
                learner_level=level,
                learner_goal=goal,
                mode=mode
            )
            st.write(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )