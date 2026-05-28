import streamlit as st
from inference_sdk import InferenceHTTPClient

def load_model():
    # Mengambil data dari Streamlit Secrets
    api_key = st.secrets["kdVsjgaJONiqFL0vcIB6"]
    verifikasi = st.secrets["baby-detector-zj9py/4"]
    prediksi = st.secrets["prediksi-usia/2""]

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com", # Gunakan endpoint ini untuk inference
        api_key=api_key
    )

    return CLIENT, verifikasi, prediksi
