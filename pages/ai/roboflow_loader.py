import streamlit as st
from inference_sdk import InferenceHTTPClient

def load_model():
    # Mengambil data dari Streamlit Secrets
    api_key = st.secrets["kdVsjgaJONiqFL0vcIB6"]
    verifikasi = st.secrets["baby-detector-zj9py/4"]
    # Tanda petik ganda di akhir sudah dihapus agar tidak error
    prediksi = st.secrets["prediksi-usia/2"] 

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com", 
        api_key=api_key
    )

    return CLIENT, verifikasi, prediksi
