import streamlit as st
import requests

st.set_page_config(
    page_title="RAG Chatbot | Organizational & Training Docs",
    page_icon="📚",
    layout="centered"
)

# --- APNA WEBHOOK YAHAN DALO ---
WEBHOOK_URL = "https://minahil111.app.n8n.cloud/webhook/3d417e7b-f21a-48ca-bcc8-04a52e239ebe/chat"

# --- CLEAN CSS ---
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .title-box {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 22px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-box p { color: #d1d5db; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="title-box">
    <h2>📚 Knowledge Assistant</h2>
    <p>Organizational Analysis • Safety Procedures • Employee Training</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR - SIRF KAAM KI CHEEZ ---
with st.sidebar:
    st.header("About This Project")
    st.write("Ye chatbot sirf neeche diye gaye 3 documents se jawab deta hai. Google se jawab nahi deta.")
    
    st.divider()
    st.subheader("📄 Documents in Database")
    st.markdown("""
    **1. Organizational Analysis Template**
    Organization ka structure, roles aur analysis kaise karte hain.

    **2. N_PR_8715_001B - Chapter 4**
    Safety, procedures aur compliance ke rules.

    **3. TalentLMS - Employee Training**
    Employee training program kaise banate hain aur manage karte hain.
    """)
    
    st.divider()
    st.subheader("💡 Kya Pooch Sakte Ho?")
    st.markdown("""
    - Organizational analysis ka process kya hai?
    - Chapter 4 me safety ke kya rules hain?
    - Employee training ke liye best steps kya hain?
    """)
    
    st.divider()
    st.caption("Tech Stack: n8n • OpenAI • Qdrant • Streamlit")
    st.caption("Developed by Minahil Ashfaq")
    
    if st.button("🗑️ Chat Clear Karo"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Assalam-o-Alaikum! 👋 Me aap ke 3 documents - Organizational Analysis, Chapter 4 aur Employee Training - se jawab dunga. Koi sawal poochein."})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Apna sawal yahan likhein...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Documents me dhoond raha hun..."):
            try:
                res = requests.post(WEBHOOK_URL, json={"question": prompt}, timeout=60)
                data = res.json()
                answer = data.get("output") or data.get("answer") or data.get("response") or str(data)
            except Exception as e:
                answer = f"Error: {e}"
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
  
