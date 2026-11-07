import streamlit as st
import requests
import uuid

N8N_URL = "https://minahil111.app.n8n.cloud/webhook/3d417e7b-f21a-48ca-bcc8-04a52e239ebe/chat"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 میرا RAG Chatbot")
st.write("اپنا سوال لکھو، جواب Qdrant والے ڈیٹا سے آئے گا۔")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("اپنا سوال یہاں لکھو..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("سوچ رہا ہوں..."):
            try:
                payload = {
                    "chatInput": question,
                    "sessionId": st.session_state.session_id
                }
                res = requests.post(N8N_URL, json=payload, timeout=120)
                data = res.json()
                answer = data.get("output", "جواب نہیں ملا، دوبارہ ٹرائی کرو")
            except Exception as e:
                answer = f"Error آ گیا: {e}"

            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
