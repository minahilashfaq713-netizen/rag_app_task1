import streamlit as st
import requests

# --- PAGE SETTING ---
st.set_page_config(
    page_title="RAG Chatbot | Minahil",
    page_icon="🤖",
    layout="centered"
)

# --- APNA WEBHOOK YAHAN DALO ---
WEBHOOK_URL = "https://minahil111.app.n8n.cloud/webhook/3d417e7b-f21a-48ca-bcc8-04a52e239ebe/chat"

# --- PROFESSIONAL CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 10px; }
    .title-box {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="title-box">
    <h1>🤖 AI Knowledge Assistant</h1>
    <p>Powered by n8n • OpenAI • Qdrant | Developed by Minahil Ashfaq</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712107.png", width=100)
    st.title("About Project")
    st.write("Ye RAG Chatbot aap ke apne documents se jawab deta hai. Ye jawab Google se nahi, aap ke Qdrant Database se uthata hai.")
    st.divider()
    st.subheader("💡 Try These Questions")
    if st.button("Qdrant kya hai?"):
        st.session_state["example"] = "Qdrant kya hai?"
    if st.button("RAG kaise kaam karta hai?"):
        st.session_state["example"] = "RAG kaise kaam karta hai?"
    if st.button("n8n workflow kya hai?"):
        st.session_state["example"] = "n8n workflow kya hai?"
    st.divider()
    if st.button("🗑️ Chat Clear Karo"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Assalam-o-Alaikum! 👋 Me aap ka AI Assistant hun. Apne documents ke bare me kuch bhi poochein."})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT ---
prompt = st.chat_input("Yahan apna sawal likhein...")

# Agar sidebar se example click hua ho
if "example" in st.session_state and st.session_state["example"]:
    prompt = st.session_state["example"]
    st.session_state["example"] = ""

if prompt:
    # User ka message dikhao
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot ka jawab lao
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hun..."):
            try:
                res = requests.post(WEBHOOK_URL, json={"question": prompt}, timeout=60)
                data = res.json()
                # n8n se jo bhi field aaye, us ko pakro
                answer = data.get("output") or data.get("answer") or data.get("response") or str(data)
            except Exception as e:
                answer = f"Error aa gaya: {e}. Please n8n check karein."
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
