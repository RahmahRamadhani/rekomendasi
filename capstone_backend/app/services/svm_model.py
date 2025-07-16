import joblib
import os
import pandas as pd

model_path = os.path.join(os.path.dirname(__file__), '..', 'ml')

svm_model = joblib.load(os.path.join(model_path, 'svm_job_predictor.pkl'))
pekerjaan_encoder = joblib.load(os.path.join(model_path, 'pekerjaan_encoder.pkl'))
_REQUIRED = ['prodi', 'jurusan', 'minat', 'skill']

def predik(record: dict) -> str:
    # pastikan semua kolom ada
    for k in _REQUIRED:
        record.setdefault(k, '')
    df = pd.DataFrame([record])
    idx  = svm_model.predict(df)[0]
    return pekerjaan_encoder.inverse_transform([idx])[0]