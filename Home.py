import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="IMUNISCAN AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS untuk menyembunyikan elemen UI default
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Selamat Datang di IMUNISCAN AI")

# NAVIGASI YANG BENAR:
# Perintah switch_page diletakkan di dalam kondisi tombol
if st.button("Masuk ke Dashboard"):
    st.switch_page("pages/dashboard.py")
