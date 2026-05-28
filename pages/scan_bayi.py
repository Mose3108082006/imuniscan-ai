import streamlit as st
from PIL import Image
import tempfile
import sys
import os

# --- PERBAIKAN IMPORT (TIDAK MENGUBAH TAMPILAN) ---
# Baris ini memastikan Python menemukan folder 'ai' dari folder 'pages'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.roboflow_loader import load_model

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="IMUNISCAN AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# SYSTEM UI CSS (TIDAK BERUBAH)
# =========================================
st.markdown("""
<style>
/* BACKGROUND UTAMA KLINIS */
.stApp {
    background: linear-gradient(180deg, #a4cbe3 0%, #bad6e7 100%) !important;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
/* SIDEBAR BIRU TUA */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d4373 0%, #0b1220 100%) !important;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
/* HEADER UTAMA */
.header {
    text-align: center;
    padding: 30px 20px;
    border-radius: 16px;
    background: linear-gradient(180deg, #1e3d6b 0%, #0f2547 100%);
    border: 1px solid #1e3a8a;
    box-shadow: 0 10px 25px rgba(13, 67, 115, 0.3);
    margin-bottom: 25px;
    width: 100%;
}
.title {
    font-size: 38px;
    font-weight: 900;
    color: #ffffff !important;
    margin: 0;
    letter-spacing: 1px;
}
.subtitle {
    margin-top: 10px;
    font-size: 15px;
    color: #93c5fd;
    font-weight: 500;
}
/* BUTTON HIJAU */
.medical-badge {
    display: inline-block;
    background-color: #16a34a;
    color: white !important;
    font-size: 11px;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 20px;
    margin-top: 15px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(22, 163, 74, 0.3);
}
/* PANEL TOP BAR */
.panel-top-bar {
    background: linear-gradient(90deg, #0d4373 0%, #1e3a8a 100%);
    color: white !important;
    padding: 12px 20px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    margin-top: 20px;
}
/* KOTAK KONTEN */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #1e3a8a !important; 
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
    border: 2px solid #38bdf8 !important; 
    border-top: none !important;
    padding: 25px !important;
    box-shadow: 0 10px 30px rgba(13, 67, 115, 0.25) !important;
}
/* TOMBOL SUBMIT */
div.stButton > button {
    background: #ffffff !important; 
    color: #1e3a8a !important; 
    font-weight: 700 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER UI
# =========================================
st.markdown("""
<div class="header">
    <div class="title">🧠 IMUNISCAN AI</div>
    <div class="subtitle">AI Vision System • Deteksi Bayi & Prediksi Usia Otomatis</div>
    <div class="medical-badge">MEDICAL AI SCAN BAYI</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# LOAD MODEL
# =========================================
CLIENT, model_verifikasi, model_usia = load_model()

# =========================================
# TABS NAVIGASI
# =========================================
tab1, tab2 = st.tabs(["📥 Input Data", "📊 Medical Report"])

# =========================================
# TAB 1: WORKSPACE UTAMA
# =========================================
with tab1:
    col1, col2 = st.columns([1, 2.2], gap="large")
    with col1:
        st.markdown('<div class="panel-top-bar">🛠️ Control Panel</div>', unsafe_allow_html=True)
        with st.container(border=True):
            metode = st.radio("Metode Input", ["Upload Foto", "Scan Kamera"], label_visibility="collapsed")
    with col2:
        st.markdown('<div class="panel-top-bar">📤 Upload Data</div>', unsafe_allow_html=True)
        with st.container(border=True):
            file = st.file_uploader("Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed") if metode == "Upload Foto" else st.camera_input("Kamera")

    if file:
        image = Image.open(file)
        st.markdown('<div class="panel-top-bar">🔮 AI Analysis</div>', unsafe_allow_html=True)
        with st.container(border=True):
            col_img, col_res = st.columns([1.1, 1.4], gap="large")
            with col_img:
                st.image(image, use_container_width=True)
            with col_res:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(file.getvalue())
                    path = tmp.name
                
                # Proses Inferensi
                res = CLIENT.infer(path, model_id=model_verifikasi)
                label = res.get("top")
                conf = res.get("confidence", 0)
                
                if label == "bayi":
                    st.success("✔ BAYI TERDETEKSI")
                else:
                    st.error("❌ BUKAN BAYI")
                    st.stop()
                
                res2 = CLIENT.infer(path, model_id=model_usia)
                usia = res2.get("top")
                conf2 = res2.get("confidence", 0)
                
                st.write(f"Usia: {usia}, Conf: {conf2}")
                st.session_state["hasil"] = {"label": label, "conf": conf, "usia": usia, "conf2": conf2, "image": image}

# =========================================
# TAB 2: MEDICAL REPORT
# =========================================
with tab2:
    if "hasil" in st.session_state:
        h = st.session_state["hasil"]
        st.write("Report Medical ditampilkan di sini.")
    else:
        st.info("Silakan unggah data di Tab 1.")
