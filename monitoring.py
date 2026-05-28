import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="IMUNISCAN AI",
    layout="wide",
    page_icon="🧠"
)

# =========================================
# SYSTEM UI CSS (SINKRONISASI TOTAL DENGAN SCAN BAYI)
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
# HEADER DISPLAY (SUDAH DISAMAKAN SAMA SCAN_BAYI)
# =========================================
st.markdown("""
<div class="header">
    <div class="title">🧠 IMUNISCAN AI</div>
    <div class="subtitle">AI Vision System • Monitoring Imunisasi </div>
    <div class="medical-badge">MEDICAL AI MONITORING</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# MASTER IMUNISASI
# =========================================
IMUNISASI = {
    "hbo < 24 jam": ("Hepatitis B", "Melindungi hepatitis B", "0 hari"),
    "hbo 1-7 hari": ("Hepatitis B lanjutan", "Imunisasi lanjutan HB", "7 hari"),
    "bcg": ("BCG", "Mencegah TBC", "1 bulan"),
    "opv 1": ("Polio", "Mencegah polio", "2 bulan"),
    "dpt-hb-hib1": ("DPT-HB-Hib", "Difteri, Tetanus, Pertusis", "2 bulan"),
    "opv 2": ("Polio", "Mencegah polio", "3 bulan"),
    "pcv 1": ("PCV", "Mencegah pneumonia", "2 bulan"),
    "rv 1": ("Rotavirus", "Mencegah diare berat", "2 bulan"),
    "dpt-hb-hib2": ("DPT-HB-Hib", "Lanjutan", "3 bulan"),
    "opv 3": ("Polio", "Mencegah polio", "4 bulan"),
    "pcv 2": ("PCV", "Lanjutan", "4 bulan"),
    "rv 2": ("Rotavirus", "Lanjutan", "4 bulan"),
    "dpt-hb-hib3": ("DPT-HB-Hib", "Lanjutan", "4 bulan"),
    "opv 4": ("Polio", "Booster", "4-5 bulan"),
    "rv 3": ("Rotavirus", "Final", "5 bulan"),
    "ipv 1": ("Polio suntik", "IPV pertama", "4-5 bulan"),
    "ipv 2": ("Polio suntik", "IPV kedua", "5-6 bulan"),
    "mr 1": ("Campak Rubella", "Imunisasi dasar MR", "9 bulan"),
    "idl": ("IDL", "Imunisasi lanjutan", "sesuai jadwal"),
    "pcv 3": ("PCV", "Booster akhir", "6-12 bulan"),
    "dpt-hb-hib4": ("DPT Booster", "Penguat kekebalan", "18 bulan"),
    "mr 2": ("MR Booster", "Penguat campak rubella", "18 bulan"),
    "ibl": ("IBL", "Imunisasi lanjutan", "sesuai jadwal"),
}

ORDER = list(IMUNISASI.keys())

# =========================================
# FUNCTIONS (LOGIKA DATA)
# =========================================
def is_filled(x):
    if pd.isna(x):
        return False
    x = str(x).strip().lower()
    return x not in ["", "nan", "none", "-", "0", "tidak", "belum"]

def load_excel():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "database", "Data Identitas Bayi dan kehaidran imunisasi.xlsx")

    if not os.path.exists(path):
        st.error("File Excel tidak ditemukan")
        return None

    df = pd.read_excel(path, engine="openpyxl", header=5)
    df.columns = df.columns.astype(str).str.lower().str.strip()
    return df

# =========================================
# INPUT FORM (KOTAK BERSIH TANPA PLACEHOLDER)
# =========================================
st.markdown('<div class="panel-top-bar">📌 Input Pencarian Data Rekam Medis Imunisasi</div>', unsafe_allow_html=True)
with st.container(border=True):
    with st.form("form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown('<div class="input-label-fix">👶 NAMA LENGKAP BAYI</div>', unsafe_allow_html=True)
            # Placeholder JIA sudah dihapus (dibuat polosan "")
            nama = st.text_input("Nama Bayi Label", label_visibility="collapsed", placeholder="")

        with col2:
            st.markdown('<div class="input-label-fix">📅 TANGGAL LAHIR</div>', unsafe_allow_html=True)
            tgl = st.date_input("Tanggal Lahir Label", datetime.today(), label_visibility="collapsed")

        st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
        
        # POLA LAYOUT BUTTON TENGAH FORM
        btn_left, btn_center, btn_right = st.columns([1, 1.3, 1])
        with btn_center:
            submit = st.form_submit_button("🔍 ANALISIS REKAM IMUNISASI")

# =========================================
# ENGINE PROSES DATA
# =========================================
if submit:
    df = load_excel()
    if df is None:
        st.stop()

    df["nama bayi"] = df["nama bayi"].astype(str).str.lower().str.strip()
    df["tanggal lahir"] = pd.to_datetime(df["tanggal lahir"], errors="coerce").dt.date

    hasil = df[
        (df["nama bayi"].str.contains(nama.lower(), na=False)) &
        (df["tanggal lahir"] == tgl)
    ]

    if hasil.empty:
        st.error("Data Rekam Medis Imunisasi tidak ditemukan. Mohon periksa kembali kriteria pencarian Anda.")
        st.stop()

    row = hasil.iloc[0]

    values = []
    for k in ORDER:
        values.append(is_filled(row.get(k, None)))

    done, missed, not_yet = [], [], []

    for i in range(len(ORDER)):
        if values[i]:
            done.append(ORDER[i])
        else:
            if any(values[i+1:]):
                missed.append(ORDER[i])
            else:
                not_yet.append(ORDER[i])

    # =========================================
    # METRICS DISPLAY COCOK & PRESISI
    # =========================================
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    c1.markdown(f"""<div class='metric-card-box' style='border-top: 4px solid #2563eb;'>
        <p style='color:#64748b; font-weight:700; margin:0; font-size:13px;'>📊 TOTAL JADWAL</p>
        <h2 class='metric-val' style='color:#2563eb;'>{len(ORDER)}</h2>
    </div>""", unsafe_allow_html=True)
    
    c2.markdown(f"""<div class='metric-card-box' style='border-top: 4px solid #16a34a;'>
        <p style='color:#64748b; font-weight:700; margin:0; font-size:13px;'>✅ SUDAH</p>
        <h2 class='metric-val' style='color:#16a34a;'>{len(done)}</h2>
    </div>""", unsafe_allow_html=True)
    
    c3.markdown(f"""<div class='metric-card-box' style='border-top: 4px solid #dc2626;'>
        <p style='color:#64748b; font-weight:700; margin:0; font-size:13px;'>⚠️ TERLEWAT</p>
        <h2 class='metric-val' style='color:#dc2626;'>{len(missed)}</h2>
    </div>""", unsafe_allow_html=True)
    
    c4.markdown(f"""<div class='metric-card-box' style='border-top: 4px solid #eab308;'>
        <p style='color:#64748b; font-weight:700; margin:0; font-size:13px;'>📅 BELUM</p>
        <h2 class='metric-val' style='color:#eab308;'>{len(not_yet)}</h2>
    </div>""", unsafe_allow_html=True)

    # =========================================
    # AREA RIWAYAT DETAIL (DATAFRAME)
    # =========================================
    st.markdown('<div class="panel-top-bar">🔮 Hasil Detail Riwayat Imunisasi</div>', unsafe_allow_html=True)
    with st.container(border=True):
        
        def render_data_table(title, data, header_bg_color):
            st.markdown(f"""<div class="table-header-title" style="background-color: {header_bg_color}; font-size:14px;">
                {title}
            </div>""", unsafe_allow_html=True)
            
            if not data:
                st.info("Tidak ada daftar rekam medis dalam kategori ini.")
                return

            rows = []
            for item in data:
                rows.append({
                    "Jenis Imunisasi": item.upper(),
                    "Manfaat / Proteksi Medis": IMUNISASI[item][1],
                    "Rekomendasi Jadwal": IMUNISASI[item][2]
                })
            df_display = pd.DataFrame(rows)
            
            st.dataframe(
                df_display, 
                use_container_width=True, 
                hide_index=True
            )
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

        render_data_table("💉 LIST VAKSINASI YANG SUDAH DIBERIKAN", done, "#16a34a")
        render_data_table("⚠️ LIST VAKSINASI YANG TERLEWAT (DIUTAMAKAN)", missed, "#dc2626")
        render_data_table("📅 LIST VAKSINASI YANG AKAN DATANG / BELUM JADWALNYA", not_yet, "#0d4373")

        # SUMMARY RESUME PASIEN BANNER
        st.markdown(f"""
        <div class="custom-success-box">
            <h4 style="color:#16a34a; margin-top:0; font-weight:700; margin-bottom:8px;">📊 Resume Pasien Berhasil Diproses</h4>
            <p style="margin: 3px 0; font-size:14px; color:#1e293b;"><b>Nama Lengkap Pasien :</b> {nama.upper()}</p>
            <p style="margin: 3px 0; font-size:14px; color:#1e293b;"><b>Tanggal Lahir :</b> {tgl.strftime('%d %B %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================================
    # PDF GENERATOR
    # =========================================
    def generate_pdf():
        file_pdf = "IMUNISCAN_REPORT.pdf"
        doc = SimpleDocTemplate(file_pdf)

        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("IMUNISCAN AI - IMMUNIZATION REPORT", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph(f"Nama Bayi: {nama}", styles["Normal"]))
        content.append(Paragraph(f"Tanggal Lahir: {tgl}", styles["Normal"]))
        content.append(Spacer(1, 10))

        def table_block(title, data):
            content.append(Paragraph(title, styles["Heading2"]))

            table = [["Imunisasi", "Manfaat", "Jadwal"]]

            for k in data:
                table.append([k, IMUNISASI[k][1], IMUNISASI[k][2]])

            t = Table(table)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
                ("PADDING", (0,0), (-1,-1), 6),
            ]))

            content.append(t)
            content.append(Spacer(1, 10))

        table_block("SUDAH IMUNISASI", done)
        table_block("TERLEWAT", missed)
        table_block("BELUM / UPCOMING", not_yet)

        doc.build(content)
        return file_pdf

    pdf_file = generate_pdf()

    # =========================================
    # ACTION DOWNLOAD BUTTON
    # =========================================
    st.markdown("<br>", unsafe_allow_html=True)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 DOWNLOAD RESUME KLINIS (PDF)",
            data=f,
            file_name=f"IMUNISCAN_{nama.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )