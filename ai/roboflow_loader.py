import streamlit as st
from inference_sdk import InferenceHTTPClient

def load_model():
    # Mengambil data dari Streamlit Secrets
    api_key = st.secrets["ROBOFLOW_API_KEY"]
    verifikasi = st.secrets["VERIFIKASI_MODEL"]
    prediksi = st.secrets["PREDIKSI_MODEL"]

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com", # Gunakan endpoint ini untuk inference
        api_key=api_key
    )

    return CLIENT, verifikasi, prediksi
