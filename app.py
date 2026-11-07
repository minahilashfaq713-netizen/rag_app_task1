import streamlit as st
import requests

st.set_page_config(
    page_title="RAG Chatbot | Knowledge Assistant",
    page_icon="📚",
    layout="centered"
)

# --- APNA WEBHOOK YAHAN DALO ---
WEBHOOK_URL = "APNA_N8N_WEBHOOK_YAHAN_PASTE_KARO"

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

# --- SIDEBAR ---
with st.sidebar:
    st.header("About This Project")
    st.write("This chatbot answers only from your uploaded documents. It does not answer from Google or general knowledge.")
    
    st.divider()
    st.subheader("What You Can Ask")
    st.markdown("""
    **1. Organizational Analysis**
    Questions related to organizational structure, roles, and analysis process.

    **2. Safety Procedures & Compliance**
    Questions related to safety rules, procedures, and compliance requirements.

    **3. Employee Training Program**
    Questions related to how to create, manage, and improve employee training programs.
    """)
    
    st.divider()
    st.caption("Tech Stack: n8n • OpenAI • Qdrant • Streamlit")
    st.caption("Developed by Minahil Ashfaq")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! 👋 You can ask me anything related to Organizational Analysis, Safety Procedures, and Employee Training Program."})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching in documents..."):
            try:
                res = requests.post(WEBHOOK_URL, json={"question": prompt}, timeout=60)
                data = res.json()
                answer = data.get("output") or data.get("answer") or data.get("response") or str(data)
            except Exception as e:
                answer = f"Error: {e}"
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})


          
  
