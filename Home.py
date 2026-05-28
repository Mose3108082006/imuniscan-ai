import streamlit as st

st.set_page_config(
    page_title="IMUNISCAN AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# hide UI Streamlit default
# PENTING: Kita tidak menyembunyikan [data-testid="stSidebar"] agar navigasi halaman tetap berfungsi
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Selamat Datang di IMUNISCAN AI")

# Tombol navigasi
# Perintah st.switch_page hanya akan diproses saat tombol ini ditekan (tidak error saat load)
if st.button("Masuk ke Dashboard"):
    st.switch_page("pages/dashboard.py")
