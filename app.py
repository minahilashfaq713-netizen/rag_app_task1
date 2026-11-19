import streamlit as st
import requests

st.set_page_config(page_title="Chatbot RAG", page_icon="🤖", layout="centered")

# 👇 اپنی n8n Production URL یہاں ڈالو
N8N_URL = "YAHAN APNI N8N URL DALO"

# Dark Theme CSS - bilkul photo jaisa
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    h1 { color: white !important; font-size: 28px !important; }
    p, label { color: #FAFAFA !important; }
    [data-testid="stFileUploader"] { background-color: #262730; border-radius: 10px; padding: 10px; }
    .success-bar { background-color: #1DB954; color: white; padding: 12px 15px; border-radius: 8px; font-weight: 600; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_done" not in st.session_state:
    st.session_state.file_done = False

# Title - Photo jaisa
st.title("Chatbot RAG")
st.write("Upload your pdf docs")

# Upload
uploaded = st.file_uploader("Drag and drop files here", type=["pdf"], label_visibility="collapsed")

if uploaded:
    # Agar pehli dafa upload hua to n8n ko bhejo
    if not st.session_state.file_done:
        with st.spinner("Uploading..."):
            files = {"data": (uploaded.name, uploaded.getvalue(), "application/pdf")}
            data = {"chatInput": f"File uploaded: {uploaded.name}"}
            try:
                r = requests.post(N8N_URL, files=files, data=data, timeout=180)
                if r.status_code == 200:
                    st.session_state.file_done = True
            except:
                pass

    st.markdown(f'<div class="success-bar">Files uploaded successfully</div>', unsafe_allow_html=True)

    # Greeting - Photo jaisa
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm the Chatbot RAG. How can I help you today?"})

# Chat dikhao
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Neeche Chat Input - Photo jaisa
if prompt := st.chat_input("what is this phd is all about and how can i apply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                r = requests.post(N8N_URL, json={"chatInput": prompt}, timeout=120)
                data = r.json()
                if isinstance(data, list):
                    reply = data[0].get("output", str(data[0]))
                else:
                    reply = data.get("output", str(data))
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")


  
    
