import streamlit as st
import requests

# Page
st.set_page_config(page_title="PDF Chat", page_icon="📄", layout="centered")

# 👇 اپنی n8n Production URL یہاں ڈالو
N8N_URL = "YAHAN APNI N8N URL DALO"

# Session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "files" not in st.session_state:
    st.session_state.files = []

# Sidebar - Sirf Upload
with st.sidebar:
    st.title("📄 PDF Chat")
    st.write("PDF سے ٹو دی پوائنٹ جواب")
    st.divider()

    uploaded = st.file_uploader("PDF اپلوڈ کرو", type=["pdf"])
    if uploaded:
        if st.button("Upload کرو", use_container_width=True, type="primary"):
            with st.spinner("اپلوڈ ہو رہا ہے..."):
                files = {"data": (uploaded.name, uploaded.getvalue(), "application/pdf")}
                data = {"chatInput": f"File uploaded: {uploaded.name}"}
                r = requests.post(N8N_URL, files=files, data=data, timeout=180)
                if r.status_code == 200:
                    if uploaded.name not in st.session_state.files:
                        st.session_state.files.append(uploaded.name)
                    st.success("ہو گیا! اب سوال پوچھو")
                else:
                    st.error("ایرر آ گیا")

    st.divider()
    st.write("**اپلوڈ ہوئی فائلیں:**")
    for f in st.session_state.files:
        st.write(f"✅ {f}")

    if st.button("چیٹ صاف کرو"):
        st.session_state.messages = []
        st.rerun()

# Main - Sirf Chat
st.title("💬 PDF سے سوال پوچھو")

if not st.session_state.files:
    st.info("👈 پہلے سائیڈ سے PDF اپلوڈ کرو، پھر سوال پوچھو")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("سوال لکھو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                r = requests.post(N8N_URL, json={"chatInput": prompt}, timeout=120)
                data = r.json()
                if isinstance(data, list):
                    reply = data[0].get("output", str(data[0]))
                else:
                    reply = data.get("output", str(data))
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"ایرر: {e}")


  
    
