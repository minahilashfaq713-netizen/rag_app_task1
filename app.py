import streamlit as st
import requests

st.set_page_config(page_title="PDF Chatbot", page_icon="📄")
st.title("📄 PDF Chatbot")
st.write("PDF اپلوڈ کرو، پھر اس سے سوال پوچھو - ٹو دی پوائنٹ جواب ملے گا۔")

# 👇 یہاں اپنی n8n والی Production URL ڈالو
N8N_URL = "YAHAN APNI N8N PRODUCTION URL PASTE KARO"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. فائل اپلوڈ والا حصہ
uploaded_file = st.file_uploader("PDF فائل یہاں اپلوڈ کرو", type=["pdf"])

if uploaded_file and st.button("فائل n8n میں بھیجو"):
    with st.spinner("فائل Qdrant میں جا رہی ہے..."):
        files = {"data": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        data = {"chatInput": "file upload"}
        res = requests.post(N8N_URL, files=files, data=data)
        if res.status_code == 200:
            st.success("فائل مل گئی ہے، یاد کر لی ہے۔ اب سوال پوچھو۔")
        else:
            st.error(f"ایرر آ گیا: {res.text}")

st.divider()

# 2. چیٹ والا حصہ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("اپنا سوال لکھو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("سوچ رہا ہوں..."):
            try:
                res = requests.post(N8N_URL, json={"chatInput": prompt}, timeout=60)
                reply = res.json().get("output", "جواب نہیں آیا")
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"ایرر: {e}")


  
    
