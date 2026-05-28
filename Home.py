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
        [data-testid="stSidebar"] {display: none;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# langsung ke dashboard
# st.switch_page("pages/dashboard.py")

st.title("Selamat Datang di IMUNISCAN AI")
if st.button("Masuk ke Dashboard"):
    st.switch_page("pages/dashboard.py")
