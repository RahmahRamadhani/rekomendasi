import joblib
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

model_path = os.path.join(os.path.dirname(__file__), '..', 'ml')
model_path = os.path.abspath(model_path)

# load data
profile_vec   = joblib.load(os.path.join(model_path, "cf_profile_vectorizer.pkl"))
raw_profiles  = joblib.load(os.path.join(model_path, "cf_raw_text_profiles.pkl"))  # list[str]
user_job_mat  = joblib.load(os.path.join(model_path, "user_job_matrix.pkl"))       # csr_matrix
label_encoder = joblib.load(os.path.join(model_path, "pekerjaan_encoder.pkl"))

def get_top_recommendations(text_profile: str, top_n: int = 5) -> list[str]:
    """
    Ambil top‑N label pekerjaan menggunakan user‑based collaborative filtering.
    text_profile  : string 'minat skill' user baru
    """
    if not text_profile.strip():
        return []

    # vektorkan profil baru
    v_new = profile_vec.transform([text_profile])

    # similarity ke seluruh user training
    sims = cosine_similarity(v_new, profile_vec.transform(raw_profiles))[0]  # shape = (n_user,)
    top_users = sims.argsort()[::-1][:10]                                    # 10 user paling mirip

    # agregasi pekerjaan user mirip
    job_sum = user_job_mat[top_users].sum(axis=0).A1                         # 1‑D array panjang n_job
    top_job_idx = job_sum.argsort()[::-1][:top_n]                            # ambil N terbanyak
    return label_encoder.inverse_transform(top_job_idx).tolist()
