import streamlit as st
from PIL import Image
import tempfile
import sys    # <--- IMPORT HARUS DI ATAS
import os     # <--- IMPORT HARUS DI ATAS
Setelah di-import, baru boleh digunakan
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.roboflow_loader import load_model

# Baru diikuti dengan kode lainnya...
st.set_page_config(...)

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="IMUNISCAN AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# SYSTEM UI CSS (PERFECT LIGHT BLUE BACKGROUND & DARK BLUE SIDEBAR)
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

/* HEADER UTAMA (UKURAN & STYLE SAMA DENGAN SCAN BAYI) */
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

/* BUTTON HIJAU DEKORATIF MEDICAL AI DASHBOARD */
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

/* PANEL TOP BAR KOTAK MONITORING */
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

/* KOTAK KONTEN FORM (WARNA SEIMBANG DAN KONTRAS) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #1e3a8a !important; 
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
    border: 2px solid #38bdf8 !important; 
    border-top: none !important;
    padding: 25px !important;
    box-shadow: 0 10px 30px rgba(13, 67, 115, 0.25) !important;
}

/* TULISAN JUDUL INPUT (HITAM PEKAT SESUAI REQUEST) */
.input-label-fix {
    font-size: 14px;
    font-weight: 700;
    color: #000000 !important; 
    margin-bottom: 8px;
    margin-top: 5px;
    letter-spacing: 0.5px;
}

/* TRANSPARENT FORM INHERITANCE */
div.stForm {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* TOMBOL SUBMIT DI TENGAH FORM */
div.stForm submit_button, div.stButton > button {
    background: #ffffff !important; 
    color: #1e3a8a !important; 
    font-weight: 700 !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    border: 1px solid #ffffff !important;
    padding: 12px 28px !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

div.stForm submit_button:hover, div.stButton > button:hover {
    background: #f8fafc !important;
    box-shadow: 0 8px 20px rgba(56, 189, 248, 0.4) !important;
    transform: translateY(-2px);
}

/* METRIC CARD */
.metric-card-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.metric-val {
    font-size: 30px;
    font-weight: 900;
    margin: 5px 0 0 0;
}

/* BOX SEKSI DATA TABEL */
.table-header-title {
    font-size: 15px;
    font-weight: 700;
    padding: 8px 12px;
    border-radius: 6px;
    color: white !important;
    margin-bottom: 12px;
}

/* SUMMARY BOX */
.custom-success-box {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
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
            st.markdown('<div class="capture-title">CAPTURE METHOD</div>', unsafe_allow_html=True)
            metode = st.radio("Metode Input", ["Upload Foto", "Scan Kamera"], label_visibility="collapsed")

    with col2:
        st.markdown('<div class="panel-top-bar">📤 Upload Data</div>', unsafe_allow_html=True)
        with st.container(border=True):
            file = st.file_uploader(
                "drag & Drop Image (JPG, JPEG, PNG)",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed"
            ) if metode == "Upload Foto" else st.camera_input("Ambil foto kamera")

    # =========================================
    # KOTAK AI ANALYSIS MELEBAR PENUH DI BAWAH
    # =========================================
    if file:
        image = Image.open(file)
        
        st.markdown('<div class="panel-top-bar">🔮 AI Analysis</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            col_img, col_res = st.columns([1.1, 1.4], gap="large")
            
            with col_img:
                st.image(image, use_container_width=True)
                st.markdown("<p style='text-align:center; color:#64748b; font-size:12px; margin-top:8px;'>Preview Gambar</p>", unsafe_allow_html=True)

            with col_res:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(file.getvalue())
                    path = tmp.name

                # ---- SUB-PROSES 1: VERIFIKASI OBJEK ----
                res = CLIENT.infer(path, model_id=model_verifikasi)
                label = res.get("top")
                conf = res.get("confidence", 0)

                st.markdown('<div class="info-section-title">🔍 Object Verification</div>', unsafe_allow_html=True)
                
                if label == "bayi":
                    st.markdown('<span class="badge-success" style="margin-bottom: 12px;">✔ BAYI TERDETEKSI</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-danger" style="margin-bottom: 12px;">❌ BUKAN BAYI</span>', unsafe_allow_html=True)
                    st.markdown('</div></div>', unsafe_allow_html=True)
                    st.stop()

                # TABEL DATA 1 (Super Kontras & Rapi)
                st.markdown(f"""
                <table style="width:100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 25px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden;">
                    <tr style="background-color: #f1f5f9; border-bottom: 1px solid #cbd5e1;">
                        <td style="padding: 10px 14px; font-weight: 600; color: #334155; width: 45%;">Parameter</td>
                        <td style="padding: 10px 14px; font-weight: 600; color: #334155;">Hasil Analisis</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0; background-color: #f8fafc;">
                        <td style="padding: 12px 14px; color: #475569;">Detected Object</td>
                        <td style="padding: 12px 14px; font-weight: 700; color: #0f172a;">{label.capitalize()}</td>
                    </tr>
                    <tr style="background-color: #ffffff;">
                        <td style="padding: 12px 14px; color: #475569;">Verification Confidence</td>
                        <td style="padding: 12px 14px; font-weight: 700; color: #16a34a;">{round(conf*100,2)}%</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)

                # ---- SUB-PROSES 2: PREDIKSI USIA ----
                res2 = CLIENT.infer(path, model_id=model_usia)
                usia = res2.get("top")
                conf2 = res2.get("confidence", 0)

                st.markdown('<div class="info-section-title">🧠 Age Prediction</div>', unsafe_allow_html=True)
                
                status_text = "INTEGRITAS TINGGI" if conf2 > 0.6 else "RENDAH"
                status_color = "#16a34a" if conf2 > 0.6 else "#dc2626"

                # TABEL DATA 2 (Zebra Striping Kontras Tinggi)
                st.markdown(f"""
                <table style="width:100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 15px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden;">
                    <tr style="background-color: #f1f5f9; border-bottom: 1px solid #cbd5e1;">
                        <td style="padding: 10px 14px; font-weight: 600; color: #334155; width: 45%;">Parameter</td>
                        <td style="padding: 10px 14px; font-weight: 600; color: #334155;">Hasil Analisis</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0; background-color: #f8fafc;">
                        <td style="padding: 12px 14px; color: #475569;">Estimated Age Bracket</td>
                        <td style="padding: 12px 14px; font-weight: 800; color: #0d4373; font-size: 15px;">{usia.replace('_', ' ')}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0; background-color: #ffffff;">
                        <td style="padding: 12px 14px; color: #475569;">Prediction Confidence</td>
                        <td style="padding: 12px 14px; font-weight: 700; color: #0f172a;">{round(conf2*100,2)}%</td>
                    </tr>
                    <tr style="background-color: #f8fafc;">
                        <td style="padding: 12px 14px; color: #475569;">Status Integritas Data</td>
                        <td style="padding: 12px 14px; font-weight: 700; color: {status_color};">{status_text}</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)
                
                st.progress(min(int(conf2 * 100), 100))

                st.session_state["hasil"] = {
                    "label": label,
                    "conf": conf,
                    "usia": usia,
                    "conf2": conf2,
                    "image": image
                }

# =========================================
# TAB 2: MEDICAL REPORT
# =========================================
with tab2:
    if "hasil" in st.session_state:
        h = st.session_state["hasil"]

        st.markdown("## 📊 Medical Report")
        st.markdown('<div class="panel-top-bar">📋 Patient & AI Diagnostics Summary</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            rep_img, rep_txt = st.columns([1, 1.5], gap="large")
            
            with rep_img:
                if h["image"]:
                    st.image(h["image"], use_container_width=True)
                    st.markdown("<p style='text-align:center; color:#64748b; font-size:12px; margin-top:8px;'>Dokumentasi Bayi Teranalisis</p>", unsafe_allow_html=True)
            
            with rep_txt:
                status_rep = "INTEGRITAS TINGGI" if h['conf2'] > 0.6 else "RENDAH"
                
                st.markdown(f"""
                <h3 style='color:#0d4373; margin-top:0; border-bottom:1px solid #cbd5e1; padding-bottom:6px;'>📌 Detection Result</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden;">
                    <tr style="background-color: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 10px 14px; color: #475569; width: 40%;">Verified Classification</td>
                        <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">: Baby Object Detected</td>
                    </tr>
                    <tr style="background-color: #ffffff;">
                        <td style="padding: 10px 14px; color: #475569;">Confidence Score</td>
                        <td style="padding: 10px 14px; font-weight: 700; color: #16a34a;">: {round(h['conf']*100,2)}%</td>
                    </tr>
                </table>
                
                <h3 style='color:#0d4373; border-bottom:1px solid #cbd5e1; padding-bottom:6px;'>🧠 AI Clinical Analysis</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 10px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden;">
                    <tr style="background-color: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 10px 14px; color: #475569; width: 40%;">Estimated Age Bracket</td>
                        <td style="padding: 10px 14px; font-weight: 800; color: #0d4373; font-size: 15px;">: {h['usia'].replace('_', ' ')}</td>
                    </tr>
                    <tr style="background-color: #ffffff; border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 10px 14px; color: #475569;">Prediction Accuracy</td>
                        <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">: {round(h['conf2']*100,2)}%</td>
                    </tr>
                    <tr style="background-color: #f8fafc;">
                        <td style="padding: 10px 14px; color: #475569;">Data Status Integrity</td>
                        <td style="padding: 10px 14px; font-weight: 700; color: #16a34a;">: {status_rep}</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)
                
        st.success("Analisis Rekam Medis AI berhasil dimuat.")
    else:
        st.info("Belum ada data analisis. Silakan unggah gambar terlebih dahulu pada tab 'Input Data'.")
