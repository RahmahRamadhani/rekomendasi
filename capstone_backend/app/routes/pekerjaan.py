from flask import Blueprint, request, jsonify
from app import db
from app.models import Pekerjaan
from datetime import datetime

pekerjaan_bp = Blueprint('pekerjaan_bp', __name__)

# ✅ GET semua pekerjaan
@pekerjaan_bp.route('/pekerjaan', methods=['GET'])
def get_all_pekerjaan():
    pekerjaan_list = Pekerjaan.query.all()
    result = []
    for p in pekerjaan_list:
        result.append({
            'id': p.id,
            'nama_pekerjaan': p.nama_pekerjaan,
            'perusahaan': p.perusahaan,
            'lokasi': p.lokasi,
            'deskripsi': p.deskripsi,
            'gaji': p.gaji,
            'tipe_pekerjaan': p.tipe_pekerjaan,
            'tanggal_ditutup': p.tanggal_ditutup.strftime('%Y-%m-%d') if p.tanggal_ditutup else None,
            'syarat': p.syarat,
            'benefit': p.benefit,
            'link_apply': p.link_apply,
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result), 200

# ✅ GET pekerjaan by ID
@pekerjaan_bp.route('/pekerjaan/<int:id>', methods=['GET'])
def get_pekerjaan(id):
    p = Pekerjaan.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'nama_pekerjaan': p.nama_pekerjaan,
        'perusahaan': p.perusahaan,
        'lokasi': p.lokasi,
        'deskripsi': p.deskripsi,
        'gaji': p.gaji,
        'tipe_pekerjaan': p.tipe_pekerjaan,
        'tanggal_ditutup': p.tanggal_ditutup.strftime('%Y-%m-%d') if p.tanggal_ditutup else None,
        'syarat': p.syarat,
        'benefit': p.benefit,
        'link_apply': p.link_apply,
    }), 200

# ✅ POST tambah pekerjaan
@pekerjaan_bp.route('/pekerjaan', methods=['POST'])
def add_pekerjaan():
    data = request.get_json()
    pekerjaan = Pekerjaan(
        nama_pekerjaan=data.get('nama_pekerjaan'),
        perusahaan=data.get('perusahaan'),
        lokasi=data.get('lokasi'),
        deskripsi=data.get('deskripsi'),
        gaji=data.get('gaji'),
        tipe_pekerjaan=data.get('tipe_pekerjaan'),
        tanggal_ditutup=datetime.strptime(data.get('tanggal_ditutup'), '%Y-%m-%d') if data.get('tanggal_ditutup') else None,
        syarat=data.get('syarat'),
        benefit=data.get('benefit'),
        link_apply=data.get('link_apply')
    )
    db.session.add(pekerjaan)
    db.session.commit()
    return jsonify({'message': 'Pekerjaan berhasil ditambahkan'}), 201