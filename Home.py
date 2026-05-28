import streamlit as st

st.set_page_config(
    page_title="IMUNISCAN AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# hide UI Streamlit default
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Selamat Datang di IMUNISCAN AI")

# --- PERBAIKAN DI SINI ---
# Gunakan st.button agar perintah pindah halaman hanya terjadi saat tombol diklik
if st.button("Masuk ke Dashboard"):
    st.switch_page("pages/dashboard.py")
