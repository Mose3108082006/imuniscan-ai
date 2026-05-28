from inference_sdk import InferenceHTTPClient

def load_model():

    api_key = open("models/api_key.txt").read().strip()

    verifikasi = open("models/verifikasi.txt").read().strip()
    prediksi = open("models/prediksi.txt").read().strip()

    CLIENT = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=api_key
    )

    return CLIENT, verifikasi, prediksi