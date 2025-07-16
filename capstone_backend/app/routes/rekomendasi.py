from flask import Blueprint, request, jsonify
from .. import db
from ..models import User, Pekerjaan, HasilRekomendasi
from ..services.svm_model import predik as prediksi_svm, pekerjaan_encoder
from ..services.cf_model import get_top_recommendations

rekomendasi_bp = Blueprint('rekomendasi_bp', __name__)

@rekomendasi_bp.route('/rekomendasi', methods=['POST'])
def rekomendasi_ksrir():
    data = request.json

    # Simpan data user
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    # --- 1. Prediksi pekerjaan utama menggunakan SVM ---
    hasil_svm = prediksi_svm({
        'prodi': data.get('prodi', ''),
        'jurusan': data.get('jurusan', ''),
        'minat': data.get('minat', ''),
        'skill': data.get('skill', '')
    })

    # --- 3. Rekomendasi CF berdasarkan text profile ---
    text_profile = f"{data.get('minat', '')} {data.get('skill', '')}".strip()
    rekomendasi_cf = get_top_recommendations(text_profile, top_n=5)

    # --- 4. Gabungkan label hasil SVM dan CF ---
    nama_pekerjaan_unik = list(set([hasil_svm] + rekomendasi_cf))

    # --- 5. Ambil lowongan berdasarkan nama pekerjaan ---
    lowongan_list = []
    for nama in nama_pekerjaan_unik:
        pekerjaan_list = Pekerjaan.query.filter_by(nama_pekerjaan=nama).all()
        for pekerjaan in pekerjaan_list:
            # Simpan rekomendasi ke tabel HasilRekomendasi
            rekom = HasilRekomendasi(user_id=user.id, pekerjaan_id=pekerjaan.id)
            db.session.add(rekom)

            lowongan_list.append({
                "id": pekerjaan.id,
                "nama_pekerjaan": pekerjaan.nama_pekerjaan,
                "perusahaan": pekerjaan.perusahaan,
                "tipe_pekerjaan": pekerjaan.tipe_pekerjaan,
                "lokasi": pekerjaan.lokasi,
                "deskripsi": pekerjaan.deskripsi
            })

    db.session.commit()
    return jsonify({
            "user": user.nama,
            "email": user.email,
            "user_id": user.id,
            "hasil_svm": hasil_svm,
            "rekomendasi_cf": rekomendasi_cf,
            "lowongan": lowongan_list,
            "status": "Rekomendasi berhasil diproses"
    }), 201

@rekomendasi_bp.route('/rekomendasi/<int:user_id>', methods=['GET'])
def get_rekomendasi(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User tidak ditemukan'}), 404

    hasil_rekomendasi = HasilRekomendasi.query.filter_by(user_id=user.id).all()
    
    lowongan_list = []
    for hasil in hasil_rekomendasi:
        pekerjaan = Pekerjaan.query.get(hasil.pekerjaan_id)
        if pekerjaan:
            lowongan_list.append({
                "id" : pekerjaan.id,
                "nama_pekerjaan": pekerjaan.nama_pekerjaan,
                "perusahaan": pekerjaan.perusahaan,
                "tipe_pekerjaan" : pekerjaan.tipe_pekerjaan,
                "lokasi": pekerjaan.lokasi,
                "deskripsi": pekerjaan.deskripsi
            })

    return jsonify({
        'user': user.nama,
        'email': user.email,
        'lowongan': lowongan_list
    }), 200
