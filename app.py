import streamlit as st
import requests
import time

# ============ PAGE SETUP ============
st.set_page_config(
    page_title="DocuChat AI - PDF Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CSS - PROFESSIONAL LOOK ============
st.markdown("""
<style>
    .main-header { font-size: 32px; font-weight: 700; color: #1A1A2E; margin-bottom: 0px; }
    .sub-header { font-size: 15px; color: #6B7280; margin-top: 5px; }
    .stButton > button { border-radius: 10px; font-weight: 600; }
    .success-box { background: #ECFDF5; padding: 12px; border-radius: 10px; border-left: 4px solid #10B981; }
    .info-box { background: #EFF6FF; padding: 12px; border-radius: 10px; border-left: 4px solid #3B82F6; }
</style>
""", unsafe_allow_html=True)

# ============ CONFIG - YAHAN APNI URL DALO ============
N8N_WEBHOOK_URL = "YAHAN APNI N8N PRODUCTION URL PASTE KARO"
# Example: https://your-n8n.app.n8n.cloud/webhook/xxxx-xxxx/chat

# ============ SESSION STATE ============
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ============ HELPER FUNCTIONS ============
def send_to_n8n_chat(message):
    """Chat message n8n ko bhejna"""
    try:
        payload = {"chatInput": message, "sessionId": st.session_state.get("session_id", "user-1")}
        res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=120)
        if res.status_code == 200:
            data = res.json()
            # n8n kabhi list deta hai, kabhi dict
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("output") or data[0].get("text") or str(data[0])
            return data.get("output") or data.get("text") or data.get("response") or str(data)
        else:
            return f"Error {res.status_code}: {res.text[:200]}"
    except Exception as e:
        return f"Connection Error: {e}"

def send_file_to_n8n(uploaded_file):
    """PDF file n8n ko bhejna"""
    try:
        files = {"data": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        data = {"chatInput": f"File uploaded: {uploaded_file.name}"}
        res = requests.post(N8N_WEBHOOK_URL, files=files, data=data, timeout=180)
        return res.status_code == 200, res.text
    except Exception as e:
        return False, str(e)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 📄 DocuChat AI")
    st.write("Apni PDF se to-the-point jawab lo.")
    st.divider()

    st.markdown("#### 📤 1. File Upload Karo")
    uploaded_file = st.file_uploader("PDF select karo", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    if uploaded_file:
        st.info(f"📎 {uploaded_file.name} - {round(uploaded_file.size/1024, 1)} KB")
        if st.button("🚀 File Upload Karo", use_container_width=True, type="primary"):
            with st.spinner("File Qdrant me ja rahi hai..."):
                success, msg = send_file_to_n8n(uploaded_file)
                if success:
                    if uploaded_file.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(uploaded_file.name)
                    st.success("✅ File yaad kar li gayi!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ Upload fail: {msg[:300]}")

    st.divider()
    st.markdown("#### 📚 Uploaded Files")
    if st.session_state.uploaded_files:
        for f in st.session_state.uploaded_files:
            st.write(f"✅ {f}")
    else:
        st.write("Abhi koi file nahi hai.")

    st.divider()
    if st.button("🗑️ Chat Clear Karo", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("#### 💡 Kaise Use Karein?")
    st.markdown("""
    1. Pehle PDF upload karo
    2. Phir neechay sawal likho
    3. Example: *Is file me kis type ka data hai?*
    4. AI sirf file se jawab dega
    """)
    st.caption("Powered by n8n + Qdrant + OpenAI")

# ============ MAIN AREA ============
st.markdown('<p class="main-header">📄 DocuChat AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Apni documents se smart, to-the-point jawab pao. Extra bakwas nahi, sirf file ka data.</p>', unsafe_allow_html=True)
st.divider()

# Quick Questions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Is file me kya hai?"):
        st.session_state.quick_q = "Is file me kis type ka data hai aur kya data hai? To the point batao."
with col2:
    if st.button("📝 Summary batao"):
        st.session_state.quick_q = "Is file ka short summary batao, to the point, bullets me."
with col3:
    if st.button("🔑 Main points kya hain?"):
        st.session_state.quick_q = "Is file ke main points kya hain? Sirf bullets me batao."

# Chat History Show
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Quick Question Handle
if "quick_q" in st.session_state and st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = ""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            reply = send_to_n8n_chat(prompt)
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Chat Input
if prompt := st.chat_input("Apna sawal likho... e.g. Is file me kya data hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            reply = send_to_n8n_chat(prompt)
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Footer
st.divider()
st.caption("⚡ Tip: Agar jawab na aaye to check karo ke n8n workflow Active hai aur Production URL sahi hai.")


  
    
