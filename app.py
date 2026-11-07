import streamlit as st
import requests
import uuid

st.set_page_config(page_title="RAG Chatbot | Knowledge Assistant", page_icon="📚", layout="centered")
WEBHOOK_URL = "https://minahil111.app.n8n.cloud/webhook/3d417e7b-f21a-48ca-bcc8-04a52e239ebe/chats"

st.markdown("""
<style>
    .title-box { background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 22px; border-radius: 12px; color: white; text-align: center; margin-bottom: 20px; }
    .title-box p { color: #d1d5db; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="title-box"><h2>📚 Knowledge Assistant</h2><p>NASA Safety • Employee Training • Organizational Analysis</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("About This Project")
    st.write("This chatbot answers only from the documents stored in the database. It does not use Google or general knowledge.")
    st.divider()
    st.subheader("What You Can Ask")
    st.markdown("""
    **1. NASA Safety & Health Programs**
    Ask about safety policies, fire protection, and institutional safety rules.

    **2. Employee Training**
    Ask about onboarding, training methods, and creating training manuals.

    **3. Organizational Analysis**
    Ask about business strategy, goals tracking, and performance analysis.
    """)
    st.divider()
    st.caption("Tech Stack: n8n • OpenAI • Qdrant • Streamlit")
    st.caption("Developed by Minahil Ashfaq")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! 👋 Ask me anything about NASA Safety, Employee Training, or Organizational Analysis."})

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
                # Chat Trigger ke liye sahi format
                payload = {
                    "action": "sendMessage",
                    "sessionId": st.session_state.session_id,
                    "chatInput": prompt
                }
                res = requests.post(WEBHOOK_URL, json=payload, timeout=120)
                data = res.json()
                # n8n Chat Trigger aksar "output" deta hai
                answer = data.get("output") or data.get("text") or data.get("response") or str(data)
            except Exception as e:
                answer = f"Error: {e}"
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})


  
    
